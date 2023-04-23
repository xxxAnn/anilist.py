from Anilist.client import Client
from Anilist.scheme.scheme import Scheme
from Anilist.vars.vars import Vars


class Query:
    """An interface to make Queries to the Anilist API
    This should usually not be used, instead use one of the subclasses

    .. warning::

        This usually should not be created manually

    :param client: A :class:`~Anilist.client.QueryClient` to make requests
    :type client: :class:`~.client.Client`
        
    :param head_name1: Name of the head :class:`~.scheme.Scheme` when in a Page object
    :type head_nama: :class:`~str`

    :param head_name2: Name of the head :class:`~.scheme.Scheme` when in a Query object
    :type head_namb: :class:`~str`

    :param defa: List of default :class:`~.scheme.Scheme`\s 
    :type defa: list[:class:`~.scheme.Scheme`]

    Example:

    .. code-block:: python

        
        client = Anilist.QueryClient()
        schs = Scheme().Media(type="$type", search="$search").sub_schemes(
            Scheme().id,
            Scheme().title.english
        )
        vars = Vars(type=AnilistMediaType("ANIME"), search="One Piece")
        result = client._request(client._create_query(vars, *schs), vars)

        # This is equivalent to using the following shortcut:
        media_search = Anilist.QueryClient().media_entry()
        media_search.search(
            Scheme().id,
            Scheme().title.english,

            type=AnilistMediaType("ANIME"),
            search="One Piece"
        )
        result = media_search.results_take_one()
    """

    def __init__(self, client: Client, head_name1, head_name2, defa):
        self._results = []
        self._client = client
        self._head_name = (head_name1, head_name2)
        self._base_schs = (Scheme()[head_name2], Scheme()[head_name1])

        self.DEFAULT_QUERY = defa

    def _query(self, *schs: Scheme, vars, head_sch, paginate=True, page=1, per_page=100):
        r = []

        if not paginate:

            q = self._client._create_query(vars, *schs, head_sch=head_sch)
            resp = self._client._request(q, vars)

            r.append(resp[self._head_name[1]])

        else:

            vars = Vars._merge(vars, Vars(page=page, perPage=per_page))
            q = self._client._create_query(vars, *schs, head_sch=Scheme._combine(Scheme().Page(page = '$page', perPage = '$perPage'), head_sch))

            r = self._client._page_request(q, vars, self._head_name[0])
        
        self._results += r

    
    def get_base_sch(self, paginate):
        return self._base_schs[0] if not paginate else self._base_schs[1]
    
    def search(self, *schs: Scheme, default=True, per_page: int=100, page: int=1, paginate=False, **kwargs):
        """Send a query to the Anilist API and add the results to the result tray

        :param schs: The Schemes to search for,
            they will be appended to the specific Query object's head :class:`~.scheme.Scheme`
        :type schs: tuple[:class:`~.scheme.Scheme`]

        *Keyword Args*: 

        :param default: Whether to add the specific Query object's default :class:`~.scheme.Scheme`\s (the default is True)
        :type default: bool, optional

        :param paginate: Whether to request a single element or pages of the element,
            if set to True then several results will be added to the result tray (the default is False)
        :type paginate: bool, optional

        :param per_page: The number of objects to query per page, this is useless if paginate is set to False (the default is 100)
        :type per_page: int, optional

        :param page: The page to start on (the default is 1)
        :type page: int, optional

        *\*\*kwargs*:
        
        The kwargs pairs are all used to create the search query,
        they are added as arguments to the specific Query object's head :class:`~.scheme.Scheme`

        For example if you are using a :class:`~.query.MediaEntryQuery`:

        .. code-block:: python

            # ... get a MediaEntryQuery
            media_search = ... # media_search is a MediaEntryQuery

            media_search.search(
                # Search schemes
                Scheme().id
                Scheme().status
                Scheme().episodes
                
                # Search parameters
                default=True
                paginate=True
                per_page=50
                page=1

                # Search arguments
                type=AnilistMediaType("ANIME")
                search="One Piece"
            )

            # This generates the following query and variables:
            #
            # Query:
            #
            # query (
            #   $type: MediaType, 
            #   $search: String, 
            #   $perPage: Int, 
            #   $page: Int
            # ) {
            #   Page (page: $page, perPage: $perPage) {
            #       media (type: $type, search: $search) {
            #           id
            #           status
            #           episodes
            #       }
            #    }
            # }
            #
            # Variables:
            #
            # {
            #   "search": "One Piece", 
            #   "type": "ANIME", 
            #   "perPage" 50, 
            #   "page": 1
            # }

        """
        # the main way to interact with this object
        vars = Vars(**kwargs)

        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        head_sch = self.get_base_sch(paginate)(**vars._as_query())
        return self._query(*schs, head_sch=head_sch, vars=vars, paginate=paginate, per_page=per_page, page=page)

    def results_take_all(self):
        """Returns the whole result tray and empties it
        """
        r = self._results
        self._results = []
        return r
    
    def results_take_front(self):
        """Returns the first element of the result tray
        and removes it from the tray.
                
        :raises KeyError: If the Query Result is empty

        :return: First element of the query's results tray
        :rtype: AnilistObject
        """
        r = self._results[0]
        self._results = self._results[1:]
        return r
    
    def results_take_back(self):
        """Returns the last element of the Query Result
        and removes it from the Query Result

        :raises KeyError: If the Query Result is empty

        :return: Last element of the query's results tray
        :rtype: :class:`AnilistObject`
        """
        r = self._results[-1]
        self._results = self._results[:-1]
        return r

