"""
    some constants for YouTube
"""

CHANNEL_RESOURCE_PROPERTIES = {
    "id",
    "brandingSettings",
    "contentDetails",
    "localizations",
    "snippet",
    "statistics",
    "status",
    "topicDetails",
}

PLAYLIST_RESOURCE_PROPERTIES = {
    "id",
    "contentDetails",
    "localizations",
    "player",
    "snippet",
    "status",
}

PLAYLIST_ITEM_RESOURCE_PROPERTIES = {"id", "contentDetails", "snippet", "status"}

VIDEO_RESOURCE_PROPERTIES = {
    "id",
    "contentDetails",
    "player",
    "snippet",
    "statistics",
    "status",
    "topicDetails",
}

RESOURCE_PARTS_MAPPING = {
    "channels": CHANNEL_RESOURCE_PROPERTIES,
    "playlists": PLAYLIST_RESOURCE_PROPERTIES,
    "playlistItems": PLAYLIST_ITEM_RESOURCE_PROPERTIES,
    "videos": VIDEO_RESOURCE_PROPERTIES,
}
