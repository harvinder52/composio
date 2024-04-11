from enum import Enum

class App(Enum):
    CLICKUP = "clickup"
    GOOGLE_DRIVE = "google-drive"
    GOOGLE_SHEETS = "google-sheets"
    MIRO = "miro"
    CALENDLY = "calendly"
    ZENDESK = "zendesk"
    ASANA = "asana"
    GITHUB = "github"
    DISCORD = "discord"
    TYPEFORM = "typeform"
    JIRA = "jira"
    TODOIST = "todoist"
    SLACK = "slack"
    TRELLO = "trello"
    GOOGLE_CALENDAR = "google-calendar"
    GOOGLE_DOCS = "google-docs"
    LINEAR = "linear"
    NOTION = "notion"
    DROPBOX = "dropbox"
    EVENTBRITE = "eventbrite"
    MIXPANEL = "mixpanel"

class TestIntegration(Enum):
    CLICKUP = "test-clickup-connector"
    GOOGLE_DRIVE = "test-google-drive-connector"
    GOOGLE_SHEETS = "test-google-sheets-connector"
    MIRO = "test-miro-connector"
    CALENDLY = "test-calendly-connector"
    ZENDESK = "test-zendesk-connector"
    ASANA = "test-asana-connector"
    GITHUB = "test-github-connector"
    DISCORD = "test-discord-connector"
    TYPEFORM = "test-typeform-connector"
    JIRA = "test-jira-connector"
    TODOIST = "test-todoist-connector"
    SLACK = "test-slack-connector"
    TRELLO = "test-trello-connector"
    GOOGLE_CALENDAR = "test-google-calendar-connector"
    GOOGLE_DOCS = "test-google-docs-connector"
    LINEAR = "test-linear-connector"
    NOTION = "test-notion-connector"
    DROPBOX = "test-dropbox-connector"
    EVENTBRITE = "test-eventbrite-connector"
    MIXPANEL = "test-mixpanel-connector"

class Action(Enum):
    def __init__(self, service, action):
        self.service = service
        self.action = action

    GMAIL_SEND_EMAIL = ("gmail", "gmail_send_email")
    GMAIL_CREATE_EMAIL_DRAFT = ("gmail", "gmail_create_email_draft")
    GMAIL_FIND_EMAIL_ID_IN_GMAIL = ("gmail", "gmail_find_email_id")
    GMAIL_ADD_LABEL_TO_EMAIL = ("gmail", "gmail_add_label_to_email")
    ZENDESK_CREATE_ZENDESK_ORGANIZATION = ("zendesk", "zendesk_create_zendesk_organization")
    ZENDESK_DELETE_ZENDESK_ORGANIZATION = ("zendesk", "zendesk_delete_zendesk_organization")
    ZENDESK_COUNT_ZENDESK_ORGANIZATIONS = ("zendesk", "zendesk_count_zendesk_organizations")
    ZENDESK_GET_ZENDESK_ORGANIZATION = ("zendesk", "zendesk_get_zendesk_organization")
    ZENDESK_GET_ZENDESK_ORGANIZATIONS = ("zendesk", "zendesk_get_all_zendesk_organizations")
    ZENDESK_UPDATE_ZENDESK_ORGANIZATION = ("zendesk", "zendesk_update_zendesk_organization")
    ZENDESK_CREATE_ZENDESK_TICKET = ("zendesk", "zendesk_create_zendesk_ticket")
    ZENDESK_DELETE_ZENDESK_TICKET = ("zendesk", "zendesk_delete_zendesk_ticket")
    ZENDESK_GET_ZENDESK_ABOUT_ME = ("zendesk", "zendesk_get_about_me")
    SLACK_SEND_SLACK_MESSAGE = ("slack", "slack_send_slack_message")
    SLACK_LIST_CHANNELS = ("slack", "slack_list_slack_channels")
    SLACK_LIST_MEMBERS = ("slack", "slack_list_slack_members")
    SLACK_LIST_MESSAGES = ("slack", "slack_list_slack_messages")
    CLICKUP_CREATE_TASK = ("clickup", "clickup_create_task")
    CLICKUP_GET_TASKS = ("clickup", "clickup_get_tasks")
    CLICKUP_GET_TASK = ("clickup", "clickup_get_task")
    CLICKUP_CREATE_LIST = ("clickup", "clickup_create_list")
    CLICKUP_GET_LISTS = ("clickup", "clickup_get_lists")
    CLICKUP_GET_SPACES = ("clickup", "clickup_get_spaces")
    CLICKUP_CREATE_SPACE = ("clickup", "clickup_create_space")
    CLICKUP_CREATE_FOLDER = ("clickup", "clickup_create_folder")
    CLICKUP_GET_FOLDERS = ("clickup", "clickup_get_folders")
    DROPBOX_GET_ABOUT_ME = ("dropbox", "dropbox_get_about_me")
    ASANA_CREATE_SUBTASK = ("asana", "asana_create_subtask")
    ASANA_GET_SUBTASKS = ("asana", "asana_get_subtasks")
    LINEAR_CREATE_ISSUE = ("linear", "linear_create_linear_issue")
    LINEAR_GET_PROJECTS = ("linear", "linear_list_linear_projects")
    LINEAR_GET_TEAMS_BY_PROJECT = ("linear", "linear_list_linear_teams")
    NOTION_GET_ABOUT_ME = ("notion", "notion_get_about_me")
    NOTION_ADD_CONTENT_NOTION_PAGE = ("notion", "notion_add_notion_page_children")
    NOTION_ARCHIVE_NOTION_PAGE = ("notion", "notion_archive_notion_page")
    NOTION_CREATE_NOTION_DATABASE = ("notion", "notion_create_notion_database")
    NOTION_CREATE_PAGE_COMMENT = ("notion", "notion_create_page_comment")
    NOTION_CREATE_NOTION_PAGE = ("notion", "notion_create_notion_page")
    NOTION_DELETE_BLOCKS = ("notion", "notion_delete_notion_page_children")
    NOTION_FETCH_ALL_UNRESOLVED_COMMENTS = ("notion", "notion_fetch_notion_comment")
    NOTION_FETCH_NOTION_DATABASE = ("notion", "notion_fetch_notion_database")
    NOTION_FETCH_NOTION_PAGE = ("notion", "notion_fetch_notion_page")
    NOTION_SEARCH_LIST_NOTION_PAGE = ("notion", "notion_search_notion_page")
    NOTION_UPDATE_NOTION_DATABASE = ("notion", "notion_update_notion_database")
    NOTION_FETCH_NOTION_BLOCKS = ("notion", "notion_fetch_notion_block")
    NOTION_FETCH_NOTION_BLOCK_CHILDREN = ("notion", "notion_fetch_notion_child_block")
    APIFY_GET_APIFY_ACTORS = ("apify", "apify_list_apify_actors")
    APIFY_CREATE_APIFY_ACTOR = ("apify", "apify_create_apify_actor")
    APIFY_GET_ACTOR_ID = ("apify", "apify_get_actor_id")
    APIFY_SEARCH_APIFY_STORE = ("apify", "apify_search_store")
    APIFY_GET_LAST_RUN_DATA = ("apify", "apify_get_last_run_data")
    APIFY_GET_APIFY_TASKS = ("apify", "apify_list_apify_tasks")
    GITHUB_CREATE_ISSUE = ("github", "github_create_issue")
    GITHUB_GET_REPOSITORY = ("github", "github_list_github_repos")
    GITHUB_STAR_REPO = ("github", "github_star_repo")
    GITHUB_GET_ABOUT_ME = ("github", "github_get_about_me")
    GITHUB_FETCH_README = ("github", "github_fetch_readme")
    GITHUB_GET_COMMITS = ("github", "github_get_commits")
    GITHUB_GET_COMMITS_WITH_PATCH_FILE_FOR_THAT_COMMIT = ("github", "github_get_commits_with_code")
    GITHUB_GET_PATCH_FOR_COMMIT = ("github", "github_get_patch_for_commit")
    TRELLO_CREATE_TRELLO_LIST = ("trello", "trello_create_trello_list")
    TRELLO_CREATE_TRELLO_CARD = ("trello", "trello_create_trello_card")
    TRELLO_GET_TRELLO_BOARD_CARDS = ("trello", "trello_get_trello_board_cards")
    TRELLO_DELETE_TRELLO_CARD = ("trello", "trello_delete_trello_card")
    TRELLO_ADD_TRELLO_CARD_COMMENT = ("trello", "trello_add_trello_card_comment")
    TRELLO_CREATE_TRELLO_LABEL = ("trello", "trello_create_trello_label")
    TRELLO_UPDATE_TRELLO_BOARD = ("trello", "trello_update_trello_board")
    TRELLO_GET_ABOUT_ME = ("trello", "trello_get_about_me")
    TRELLO_SEARCH_TRELLO = ("trello", "trello_search_trello")
    TRELLO_SEARCH_TRELLO_MEMBERS = ("trello", "trello_search_trello_member")
    TRELLO_UPDATE_TRELLO_CARD = ("trello", "trello_update_trello_card")
    TYPEFORM_GET_ABOUT_ME = ("typeform", "typeform_get_about_me")

class Trigger(Enum):
    def __init__(self, service, trigger):
        self.service = service
        self.trigger = trigger

    SLACK_NEW_MESSAGE = ("slack", "slack_receive_message")
    GITHUB_PULL_REQUEST_EVENT = ("github", "github_pull_request_event")
    GITHUB_COMMIT_EVENT = ("github", "github_commit_event")
