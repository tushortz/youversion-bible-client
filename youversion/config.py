"""Configuration constants for YouVersion API client."""


class Config:
    """Configuration constants."""

    # API Configuration
    BASE_URL = "https://my.bible.com"
    BIBLE_COM_BASE_URL = "https://www.bible.com"
    VOTD_URL = "https://nodejs.bible.com/api/moments/votd/3.1"

    # YouVersion API Base URLs
    AUDIO_BIBLE_API_BASE = "http://audio-bible.youversionapi.com"
    BADGES_API_BASE = "https://badges.youversionapi.com"
    BIBLE_API_BASE = "https://bible.youversionapi.com"
    EVENTS_API_BASE = "https://events.youversionapi.com"
    FRIENDS_API_BASE = "https://friends.youversionapi.com"
    FRIENDSHIPS_API_BASE = "https://friendships.youversionapi.com"
    IMAGES_API_BASE = "https://images.youversionapi.com"
    MOMENTS_API_BASE = "https://moments.youversionapi.com"
    NOTIFICATIONS_API_BASE = "https://notifications.youversionapi.com"
    SEARCH_API_BASE = "https://search.youversionapi.com"
    SHARE_API_BASE = "https://share.youversionapi.com"
    THEMES_API_BASE = "https://themes.youversionapi.com"
    VIDEOS_API_BASE = "https://videos.youversionapi.com"
    YOUVERSION_API_BASE = "https://youversionapi.com"

    # OAuth2 Configuration
    AUTH_URL = "https://auth.youversionapi.com/token"
    CLIENT_ID = "ODViNjFkOTdhNzliOTZiZTQ2NWViYWVlZTgzYjEzMTM="
    CLIENT_SECRET = "NzVjZjBlMTQxY2JmNDFlZjQxMGFkY2U1YjY1MzdhNDk="

    # API Headers
    DEFAULT_HEADERS = {
        "Referer": "http://android.youversionapi.com/",
        "X-YouVersion-App-Platform": "android",
        "X-YouVersion-App-Version": "17114",
        "X-YouVersion-Client": "youversion",
    }

    # Endpoints
    SIGNIN_URL = "/sign-in"

    # Bible API Endpoints
    BIBLE_CHAPTER_URL = "/3.1/chapter.json"
    BIBLE_CONFIGURATION_URL = "/3.1/configuration.json"
    BIBLE_RECOMMENDED_LANGUAGES_URL = "/3.1/recommended_languages.json"
    BIBLE_VERSION_URL = "/3.1/version.json"
    BIBLE_VERSIONS_URL = "/3.1/versions.json"

    # Audio Bible API Endpoints
    AUDIO_CHAPTER_URL = "/3.1/chapter.json"
    AUDIO_VIEW_URL = "/3.1/view.json"

    # Friends API Endpoints
    FRIENDS_ALL_ITEMS_URL = "/3.1/all_items.json"
    FRIENDS_DELETE_URL = "/3.1/delete.json"
    FRIENDS_ITEMS_URL = "/3.1/items.json"
    FRIENDSHIPS_ACCEPT_URL = "/3.1/accept.json"
    FRIENDSHIPS_CONTACTS_URL = "/3.1/contacts.json"
    FRIENDSHIPS_DECLINE_URL = "/3.1/decline.json"
    FRIENDSHIPS_DISMISS_SUGGESTION_URL = "/3.1/dismiss_suggestion.json"
    FRIENDSHIPS_FACEBOOK_FRIENDS_URL = "/3.1/facebook_friends.json"
    FRIENDSHIPS_INCOMING_URL = "/3.1/incoming.json"
    FRIENDSHIPS_OFFER_URL = "/3.1/offer.json"
    FRIENDSHIPS_SUGGESTIONS_URL = "/3.1/suggestions.json"
    SHARE_INVITE_EMAIL_URL = "/3.1/invite_email.json"
    SHARE_INVITE_SMS_URL = "/3.1/invite_sms.json"

    # Events API Endpoints
    EVENTS_CONFIGURATION_URL = "/3.2/configuration.json"
    EVENTS_DELETE_SAVED_URL = "/3.2/delete_saved.json"
    EVENTS_SAVE_URL = "/3.2/save.json"
    EVENTS_SAVED_ALL_ITEMS_URL = "/3.2/saved_all_items.json"
    EVENTS_SAVED_ITEMS_URL = "/3.2/saved_items.json"
    EVENTS_SEARCH_URL = "/3.2/search.json"
    EVENTS_VIEW_URL = "/3.2/view.json"

    # Search API Endpoints
    SEARCH_BIBLE_URL = "/3.1/bible.json"
    SEARCH_PLANS_URL = "/3.1/plans.json"
    SEARCH_SUGGEST_URL = "/3.1/suggest.json"
    SEARCH_USERS_URL = "/3.1/users.json"
    SEARCH_VIDEOS_URL = "/3.1/videos.json"

    # Videos API Endpoints
    VIDEOS_VIEW_URL = "/3.1/view.json"

    # Badges API Endpoints
    BADGES_ITEMS_URL = "/3.1/items.json"

    # Images API Endpoints
    IMAGES_ITEMS_URL = "/3.1/items.json"
    IMAGES_UPLOAD_URL = "/3.1/upload.json"

    # Notifications API Endpoints
    NOTIFICATIONS_ITEMS_URL = "/3.1/items.json"
    NOTIFICATIONS_SETTINGS_URL = "/3.1/settings.json"
    NOTIFICATIONS_UPDATE_SETTINGS_URL = "/3.1/update_settings.json"
    NOTIFICATIONS_UPDATE_URL = "/3.1/update.json"
    NOTIFICATIONS_UPDATE_VOTD_SETTINGS_URL = "/3.1/update_votd_settings.json"
    NOTIFICATIONS_VOTD_SETTINGS_URL = "/3.1/votd_settings.json"

    # Moments API Endpoints
    MOMENTS_CLIENT_SIDE_ITEMS_URL = "/3.1/client_side_items.json"
    MOMENTS_COLORS_URL = "/3.1/colors.json"
    MOMENTS_CONFIGURATION_URL = "/3.1/configuration.json"
    MOMENTS_CREATE_URL = "/3.1/create.json"
    MOMENTS_DELETE_URL = "/3.1/delete.json"
    MOMENTS_HIDE_VERSE_COLORS_URL = "/3.1/hide_verse_colors.json"
    MOMENTS_ITEMS_URL = "/3.1/items.json"
    MOMENTS_LABELS_URL = "/3.1/labels.json"
    MOMENTS_SEARCH_URL = "/3.1/search/moments.json"
    MOMENTS_UPDATE_URL = "/3.1/update.json"
    MOMENTS_VERSE_COLORS_URL = "/3.1/verse_colors.json"
    MOMENTS_VIEW_URL = "/3.1/view.json"
    MOMENTS_VOTD_URL = "/3.1/votd.json"

    # Comments API Endpoints
    COMMENTS_CREATE_URL = "/3.1/comments/create.json"
    COMMENTS_DELETE_URL = "/3.1/comments/delete.json"

    # Likes API Endpoints
    LIKES_CREATE_URL = "/3.1/likes/create.json"
    LIKES_DELETE_URL = "/3.1/likes/delete.json"

    # Messaging API Endpoints
    MESSAGING_REGISTER_URL = "/3.1/messaging/register.json"
    MESSAGING_UNREGISTER_URL = "/3.1/messaging/unregister.json"

    # Themes API Endpoints
    THEMES_ADD_URL = "/3.1/create.json"
    THEMES_DESCRIPTION_URL = "/3.1/description.json"
    THEMES_ITEMS_URL = "/3.1/items.json"
    THEMES_REMOVE_URL = "/3.1/remove.json"
    THEMES_SET_URL = "/3.1/set.json"

    # Localization API Endpoints
    LOCALIZATION_ITEMS_URL = "/3.1/localization/items.po"

    # Alternative endpoints without build ID
    READING_PLANS_URL = "/users/{username}/reading-plans"
    USER_PROFILE_URL = "/users/{username}"

    # HTTP Configuration
    HTTP_TIMEOUT = 30.0

    # Pagination
    DEFAULT_PAGE = 1
    DEFAULT_LIMIT = 10
