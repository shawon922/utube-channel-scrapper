"""
    Main Api implementation.
"""

from typing import Optional, List, Union

import requests
from requests.models import Response

from utube.utilz.params_checker import enf_comma_separated, enf_parts


class Api(object):
    """
    Example usage:
        To create an instance of pyyoutube.Api class:

            >>> from utube.scrapper.api import Api
            >>> api = Api(api_key="your api key")

        To get one channel info:

            >>> res = api.get_channel_info(channel_name="googledevelopers")
            >>> print(res.items[0])

        Now this api provide methods as follows:
            >>> api.get_channel_info()
            >>> api.get_playlist_by_id()
            >>> api.get_playlists()
            >>> api.get_playlist_item_by_id()
            >>> api.get_playlist_items()
            >>> api.get_video_by_id()
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3/"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
    ) -> None:
        """
        This Api provide two method to work. Use api key or use access token.

        Args:
            api_key(str, optional):
                The api key which you create from google api console.
            timeout(int, optional):
                The request timeout.
            proxies(dict, optional):
                If you want use proxy, need point this param.
                param style like requests lib style.
                Refer https://2.python-requests.org//en/latest/user/advanced/#proxies

        Returns:
            Api instance.
        """

        self._api_key = api_key
        self.session = requests.Session()
        self._timeout = 10
        self.proxies = proxies
        self.scope = None

    @staticmethod
    def _parse_response(response: Response) -> dict:
        """
        Parse response data and check whether errors exists.

        Args:
            response (Response)
                The response which the request return.
        Return:
             response's data
        """
        data = response.json()
        if "error" in data:
            raise Exception(response)
        return data

    @staticmethod
    def _parse_data(data: Optional[dict]) -> Union[dict, list]:
        """
        Parse resp data.

        Args:
            data (dict)
                The response data by response.json()
        Return:
             response's items
        """
        items = data["items"]
        return items

    def _request(
        self, resource, method=None, args=None, post_args=None
    ) -> Response:
        """
        Main request sender.

        Args:
            resource(str)
                Resource field is which type data you want to retrieve.
                Such as channels，videos and so on.
            method(str, optional)
                The method this request to send request.
                Default is 'GET'
            args(dict, optional)
                The url params for this request.
            post_args(dict, optional)
                The Post params for this request.
        Returns:
            response
        """
        if method is None:
            method = "GET"

        if args is None:
            args = dict()

        if post_args is not None:
            method = "POST"

        key = None
        access_token = None
        if self._api_key is not None:
            key = "key"
            access_token = self._api_key

        if method == "POST" and key not in post_args:
            post_args[key] = access_token
        elif method == "GET" and key not in args:
            args[key] = access_token

        try:
            response = self.session.request(
                method=method,
                url=self.BASE_URL + resource,
                timeout=self._timeout,
                params=args,
                data=post_args,
                proxies=self.proxies,
            )
        except requests.HTTPError as e:
            raise Exception(message=e.args[0])
        else:
            return response

    def get_channel_info(
        self,
        *,
        channel_id: Optional[Union[str, list, tuple, set]] = None,
        channel_name: Optional[str] = None,
        mine: Optional[bool] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: str = "en_US",
    ):
        """
        Retrieve channel data from YouTube Data API.

        Note:
            1. Don't know why, but now you could't get channel list by given an guide category.
               You can only get list by parameters mine,forUsername,id.
               Refer: https://developers.google.com/youtube/v3/guides/implementation/channels
            2. The origin maxResult param not work for these filter method.

        Args:
            channel_id ((str,list,tuple,set), optional):
                The id or comma-separated id string for youtube channel which you want to get.
                You can also pass this with an id list, tuple, set.
            channel_name (str, optional):
                The name for youtube channel which you want to get.
            mine (bool, optional):
                If you have give the authorization. Will return your channels.
                Must provide the access token.
            parts (str, optional):
                Comma-separated list of one or more channel resource properties.
                If not provided. will use default public properties.
            hl (str, optional):
                If provide this. Will return channel's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.

        Returns:
            data
        """

        args = {
            "part": enf_parts(resource="channels", value=parts),
            "hl": hl,
        }
        if channel_name is not None:
            args["forUsername"] = channel_name
        elif channel_id is not None:
            args["id"] = enf_comma_separated("channel_id", channel_id)
        elif mine is not None:
            args["mine"] = mine
        else:
            raise Exception("Specify at least one of channel_id,channel_name or mine")

        resp = self._request(resource="channels", method="GET", args=args)

        return self._parse_response(resp)

    def paged_by_page_token(
            self, resource: str, args: dict, count: Optional[int] = None,
    ):
        """
        Response paged by response's page token. If not provide response token
        Args:
            resource (str):
                The resource string need to retrieve data.
            args (dict)
                The args for api.
            count (int, optional):
                The count for result items you want to get.
                If provide this with None, will retrieve all items.
                Note:
                    The all items maybe too much. Notice your app's cost.
        Returns:
            Data api origin response.
        """
        res_data: Optional[dict] = None
        current_items: List[dict] = []
        page_token: Optional[str] = None
        now_items_count: int = 0

        while True:
            if page_token is not None:
                args["pageToken"] = page_token

            resp = self._request(resource=resource, method="GET", args=args)
            data = self._parse_response(resp)  # origin response
            # set page token
            page_token = data.get("nextPageToken")
            prev_page_token = data.get("prevPageToken")

            # parse results.
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            # first check the count if satisfies.
            if count is not None:
                if now_items_count >= count:
                    current_items = current_items[:count]
                    break
            # if have no page token, mean no more data.
            if page_token is None:
                break
        res_data["items"] = current_items

        # use last request page token
        res_data["nextPageToken"] = page_token
        res_data["prevPageToken"] = prev_page_token
        return res_data

    def get_playlist_by_id(
        self,
        *,
        playlist_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
    ):
        """
        Retrieve playlist data by given playlist id.

        Args:
            playlist_id ((str,list,tuple,set)):
                The id for playlist that you want to retrieve data.
                You can pass this with single id str,comma-separated id str, or list, tuple, set of id str.
            parts (str, optional):
                Comma-separated list of one or more playlist resource properties.
                You can also pass this with list, tuple, set of part str.
                If not provided. will use default public properties.
            hl (str, optional):
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
        Returns:
            data
        """
        args = {
            "id": enf_comma_separated("playlist_id", playlist_id),
            "part": enf_parts(resource="playlists", value=parts),
            "hl": hl,
        }

        resp = self._request(resource="playlists", method="GET", args=args)

        return self._parse_response(resp)

    def get_playlists(
        self,
        *,
        channel_id: Optional[str] = None,
        mine: Optional[bool] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        count: Optional[int] = 5,
        limit: Optional[int] = 5,
        hl: Optional[str] = "en_US",
        page_token: Optional[str] = None,
    ):
        """
        Retrieve channel playlists info from youtube data api.

        Args:
            channel_id (str, optional):
                If provide channel id, this will return pointed channel's playlist info.
            mine (bool, optional):
                If you have given the authorization. Will return your playlists.
                Must provide the access token.
            parts (str, optional):
                Comma-separated list of one or more playlist resource properties.
                You can also pass this with list, tuple, set of part str.
                If not provided. will use default public properties.
            count (int, optional):
                The count will retrieve playlist data.
                Default is 5.
                If provide this with None, will retrieve all playlists.
            limit (int, optional):
                The maximum number of items each request to retrieve.
                For playlist, this should not be more than 50.
                Default is 5
            hl (str, optional):
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            page_token(str, optional):
                The token of the page of playlists result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
        Returns:
            data
        """

        if count is None:
            limit = 50  # for playlists the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "part": enf_parts(resource="playlists", value=parts),
            "hl": hl,
            "maxResults": limit,
        }

        if channel_id is not None:
            args["channelId"] = channel_id
        elif mine is not None:
            args["mine"] = mine
        else:
            raise Exception("Specify at least one of channel_id,playlist_id or mine")

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="playlists", args=args, count=count
        )

        return res_data

    def get_playlist_item_by_id(
        self,
        *,
        playlist_item_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
    ):
        """
        Retrieve playlist Items info by your given id

        Args:
            playlist_item_id ((str,list,tuple,set)):
                The id for playlist item that you want to retrieve info.
                You can pass this with single id str, comma-separated id str.
                Or a list,tuple,set of ids.
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
        Returns:
            data
        """

        args = {
            "id": enf_comma_separated("playlist_item_id", playlist_item_id),
            "part": enf_parts(resource="playlistItems", value=parts),
        }

        resp = self._request(resource="playlistItems", method="GET", args=args)

        return self._parse_response(resp)

    def get_playlist_items(
        self,
        *,
        playlist_id: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        video_id: Optional[str] = None,
        count: Optional[int] = 5,
        limit: Optional[int] = 5,
        page_token: Optional[str] = None,
    ):
        """
        Retrieve playlist Items info by your given playlist id

        Args:
            playlist_id (str):
                The id for playlist that you want to retrieve items data.
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            video_id (str, Optional):
                Specifies that the request should return only the playlist items that contain the specified video.
            count (int, optional):
                The count will retrieve playlist items data.
                Default is 5.
                If provide this with None, will retrieve all playlist items.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For playlistItem, this should not be more than 50.
                Default is 5
            page_token(str, optional):
                The token of the page of playlist items result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
        Returns:
            data
        """

        if count is None:
            limit = 50  # for playlistItems the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "playlistId": playlist_id,
            "part": enf_parts(resource="playlistItems", value=parts),
            "maxResults": limit,
        }
        if video_id is not None:
            args["videoId"] = video_id

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="playlistItems", args=args, count=count
        )

        return res_data

    def get_video_by_id(
        self,
        *,
        video_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        limit: Optional[int] = 10,
    ):
        """
        Retrieve video data by given video id.

        Args:
            video_id ((str,list,tuple,set)):
                The id for video that you want to retrieve data.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            limit (int, optional):
                The maximum number of items each request retrieve.
        Returns:
            data
        """

        args = {
            "id": enf_comma_separated(field="video_id", value=video_id),
            "part": enf_parts(resource="videos", value=parts),
            "maxResults": limit,
        }

        resp = self._request(resource="videos", method="GET", args=args)

        return self._parse_response(resp)

