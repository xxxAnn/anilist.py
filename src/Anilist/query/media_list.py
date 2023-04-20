class MediaListQuery:
    
    def __init__(self, client, username: str, per_page: int=10, starting_page: int = 1, languages=["english"]):
        self._username = username
        self._per_page = per_page
        self._starting_page = starting_page
        self._languages = languages
        self._client = client
        self._media_entries = []
        # load a few important values
        self._base_query()

    @property
    def entries(self):
        return self._media_entries

    def _base_query(self):
        query = """
        query ($usr: String, $page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                mediaList (userName: $usr) {
                    media {
                        id
                        title {
                            {0}
                        }
                        coverImage {
                            extraLarge
                            large
                            medium
                        }
                    }
                }
            }
        }
        """.format('\n'.join(self._languages))

        vars = {
            "usr": self._username,
            "page": self._starting_page,
            "perPage": self._per_page
        }

        pg = self._starting_page
        temp = []

        while True:
            resp = self._client._request(query, vars=vars)
            data = ([v.media for v in resp.Page.mediaList])

            temp.extend(data)

            if data == []:
                break

            pg += 1
            vars["page"] = pg

        self._media_entries = temp
