from Anilist.client import Client
from Anilist.scheme.scheme import Scheme
from Anilist.vars.vars import Vars


class Query:
    """
    An interface to make Queries to the Anilist API

    ...

    Methods
    -------
    results_take_all()
        Returns the Query Result

    results_take_front()
        Returns the first element of the Query Result

    results_take_back()
        Returns the last element of the Query Result
    """

    def __init__(self, client: Client, head_name, scha, schb, defa):
        self._results = []
        self._client = client
        self._head_name = head_name
        self._base_schs = (scha, schb)

        self.DEFAULT_QUERY = defa

    def _query(self, *schs: Scheme, vars, head_sch, paginate=True, page=1, per_page=100):
        r = []

        if not paginate:

            q = self._client._create_query(vars, *schs, head_sch=head_sch)
            resp = self._client._request(q, vars._json)

            r.append(resp.Media)

        else:

            vars = Vars._merge(vars, Vars(page=page, perPage=per_page))
            q = self._client._create_query(vars, *schs, head_sch=Scheme._combine(Scheme().Page(page = '$page', perPage = '$perPage'), head_sch))

            r = self._client._page_request(q, vars, self._head_name)
        
        self._results = r

    
    def query(self, *schs: Scheme, vars, head_sch=Scheme(), default=True, paginate=False, page=1, per_page=100):
        # this is for interacting in the most direct way with the Internal API 
        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        return self._query(*schs, vars=vars,  head_sch=head_sch, paginate=paginate, page=page, per_page=per_page)
    
    def get_base_sch(self, paginate):
        return self._base_schs[0] if not paginate else self._base_schs[1]
    
    def search(self, *schs: Scheme, default=True, per_page: int=100, page: int=1, paginate=False, **kwargs):
        # the main way to interact with this object
        vars = Vars(**kwargs)

        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        head_sch = self.get_base_sch(paginate)(**vars._as_query())
        return self._query(*schs, head_sch=head_sch, vars=vars, paginate=paginate, per_page=per_page, page=page)

    def results_take_all(self):
        """Returns the Query Result
        and empties it.
        """
        r = self._results
        self._results = []
        return r
    
    def results_take_front(self):
        """Returns the first element of the Query Result
        and removes it from the Query Result.

        Raises
        ------
        KeyError
            If the Query Result is empty.
        """
        r = self._results[0]
        self._results = self._results[1:]
        return r
    
    def results_take_back(self):
        """Returns the last element of the Query Result
        and removes it from the Query Result.

        Raises
        ------
        KeyError
            If the Query Result is empty.
        """
        r = self._results[-1]
        self._results = self._results[:-1]
        return r

