class MediaEntryMutable:
    
    def __init__(self, id, client):
        self._id = id
        self._client = client

    def set_score(self, score):
        query = """
        mutation ($id: Int, $score: Float) {
            SaveMediaListEntry (id: $id, score: $score) {
                id
                score
            }
        }
        """

        resp = self._client._request(query, vars={
            "id": self._id,
            "score": score
        })

        return "OK"
    
    def delete(self):
        query = """
        mutation ($id: Int) {
            DeleteMediaListEntry (id: $id) {
                deleted
            }
        }
        """

        resp = self._client._request(query, vars={
            "id": self._id,
        })

        if resp.DeleteMediaListEntry.deleted:
            return "OK"
        else:
            return "ERR"

    @classmethod
    def _from_media_id(cls, client, media_id):
        query = """
        mutation ($mediaId: Int) {
            SaveMediaListEntry (mediaId: $mediaId) {
                id
            }
        }
        """

        resp = client._request(query, vars={
            "mediaId": media_id
        })

        return cls(resp.SaveMediaListEntry.id, client)
