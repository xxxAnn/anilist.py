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

    def __init__(self):
        self._results = []

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

