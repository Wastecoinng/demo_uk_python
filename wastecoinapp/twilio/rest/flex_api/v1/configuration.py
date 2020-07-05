# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class ConfigurationList(ListResource):
    """  """

    def __init__(self, version):
        """
        Initialize the ConfigurationList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.flex_api.v1.configuration.ConfigurationList
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationList
        """
        super(ConfigurationList, self).__init__(version)

        # Path Solution
        self._solution = {}

    def get(self):
        """
        Constructs a ConfigurationContext

        :returns: twilio.rest.flex_api.v1.configuration.ConfigurationContext
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationContext
        """
        return ConfigurationContext(self._version, )

    def __call__(self):
        """
        Constructs a ConfigurationContext

        :returns: twilio.rest.flex_api.v1.configuration.ConfigurationContext
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationContext
        """
        return ConfigurationContext(self._version, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.FlexApi.V1.ConfigurationList>'


class ConfigurationPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the ConfigurationPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.flex_api.v1.configuration.ConfigurationPage
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationPage
        """
        super(ConfigurationPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of ConfigurationInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        return ConfigurationInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.FlexApi.V1.ConfigurationPage>'


class ConfigurationContext(InstanceContext):
    """  """

    def __init__(self, version):
        """
        Initialize the ConfigurationContext

        :param Version version: Version that contains the resource

        :returns: twilio.rest.flex_api.v1.configuration.ConfigurationContext
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationContext
        """
        super(ConfigurationContext, self).__init__(version)

        # Path Solution
        self._solution = {}
        self._uri = '/Configuration'.format(**self._solution)

    def fetch(self, ui_version=values.unset):
        """
        Fetch the ConfigurationInstance

        :param unicode ui_version: The Pinned UI version of the Configuration resource to fetch

        :returns: The fetched ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        data = values.of({'UiVersion': ui_version, })

        payload = self._version.fetch(method='GET', uri=self._uri, params=data, )

        return ConfigurationInstance(self._version, payload, )

    def create(self):
        """
        Create the ConfigurationInstance

        :returns: The created ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        payload = self._version.create(method='POST', uri=self._uri, )

        return ConfigurationInstance(self._version, payload, )

    def update(self):
        """
        Update the ConfigurationInstance

        :returns: The updated ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        payload = self._version.update(method='POST', uri=self._uri, )

        return ConfigurationInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.FlexApi.V1.ConfigurationContext {}>'.format(context)


class ConfigurationInstance(InstanceResource):
    """  """

    class Status(object):
        OK = "ok"
        INPROGRESS = "inprogress"
        NOTSTARTED = "notstarted"

    def __init__(self, version, payload):
        """
        Initialize the ConfigurationInstance

        :returns: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        super(ConfigurationInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'attributes': payload.get('attributes'),
            'status': payload.get('status'),
            'taskrouter_workspace_sid': payload.get('taskrouter_workspace_sid'),
            'taskrouter_target_workflow_sid': payload.get('taskrouter_target_workflow_sid'),
            'taskrouter_target_taskqueue_sid': payload.get('taskrouter_target_taskqueue_sid'),
            'taskrouter_taskqueues': payload.get('taskrouter_taskqueues'),
            'taskrouter_skills': payload.get('taskrouter_skills'),
            'taskrouter_worker_channels': payload.get('taskrouter_worker_channels'),
            'taskrouter_worker_attributes': payload.get('taskrouter_worker_attributes'),
            'taskrouter_offline_activity_sid': payload.get('taskrouter_offline_activity_sid'),
            'runtime_domain': payload.get('runtime_domain'),
            'messaging_service_instance_sid': payload.get('messaging_service_instance_sid'),
            'chat_service_instance_sid': payload.get('chat_service_instance_sid'),
            'flex_service_instance_sid': payload.get('flex_service_instance_sid'),
            'ui_language': payload.get('ui_language'),
            'ui_attributes': payload.get('ui_attributes'),
            'ui_dependencies': payload.get('ui_dependencies'),
            'ui_version': payload.get('ui_version'),
            'service_version': payload.get('service_version'),
            'call_recording_enabled': payload.get('call_recording_enabled'),
            'call_recording_webhook_url': payload.get('call_recording_webhook_url'),
            'crm_enabled': payload.get('crm_enabled'),
            'crm_type': payload.get('crm_type'),
            'crm_callback_url': payload.get('crm_callback_url'),
            'crm_fallback_url': payload.get('crm_fallback_url'),
            'crm_attributes': payload.get('crm_attributes'),
            'public_attributes': payload.get('public_attributes'),
            'plugin_service_enabled': payload.get('plugin_service_enabled'),
            'plugin_service_attributes': payload.get('plugin_service_attributes'),
            'integrations': payload.get('integrations'),
            'outbound_call_flows': payload.get('outbound_call_flows'),
            'serverless_service_sids': payload.get('serverless_service_sids'),
            'wfm_integrations': payload.get('wfm_integrations'),
            'queue_stats_configuration': payload.get('queue_stats_configuration'),
            'url': payload.get('url'),
        }

        # Context
        self._context = None
        self._solution = {}

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: ConfigurationContext for this ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationContext
        """
        if self._context is None:
            self._context = ConfigurationContext(self._version, )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created the resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def date_created(self):
        """
        :returns: The ISO 8601 date and time in GMT when the Configuration resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The ISO 8601 date and time in GMT when the Configuration resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def attributes(self):
        """
        :returns: An object that contains application-specific data
        :rtype: dict
        """
        return self._properties['attributes']

    @property
    def status(self):
        """
        :returns: The status of the Flex onboarding
        :rtype: ConfigurationInstance.Status
        """
        return self._properties['status']

    @property
    def taskrouter_workspace_sid(self):
        """
        :returns: The SID of the TaskRouter Workspace
        :rtype: unicode
        """
        return self._properties['taskrouter_workspace_sid']

    @property
    def taskrouter_target_workflow_sid(self):
        """
        :returns: The SID of the TaskRouter target Workflow
        :rtype: unicode
        """
        return self._properties['taskrouter_target_workflow_sid']

    @property
    def taskrouter_target_taskqueue_sid(self):
        """
        :returns: The SID of the TaskRouter Target TaskQueue
        :rtype: unicode
        """
        return self._properties['taskrouter_target_taskqueue_sid']

    @property
    def taskrouter_taskqueues(self):
        """
        :returns: The list of TaskRouter TaskQueues
        :rtype: dict
        """
        return self._properties['taskrouter_taskqueues']

    @property
    def taskrouter_skills(self):
        """
        :returns: The Skill description for TaskRouter workers
        :rtype: dict
        """
        return self._properties['taskrouter_skills']

    @property
    def taskrouter_worker_channels(self):
        """
        :returns: The TaskRouter default channel capacities and availability for workers
        :rtype: dict
        """
        return self._properties['taskrouter_worker_channels']

    @property
    def taskrouter_worker_attributes(self):
        """
        :returns: The TaskRouter Worker attributes
        :rtype: dict
        """
        return self._properties['taskrouter_worker_attributes']

    @property
    def taskrouter_offline_activity_sid(self):
        """
        :returns: The TaskRouter SID of the offline activity
        :rtype: unicode
        """
        return self._properties['taskrouter_offline_activity_sid']

    @property
    def runtime_domain(self):
        """
        :returns: The URL where the Flex instance is hosted
        :rtype: unicode
        """
        return self._properties['runtime_domain']

    @property
    def messaging_service_instance_sid(self):
        """
        :returns: The SID of the Messaging service instance
        :rtype: unicode
        """
        return self._properties['messaging_service_instance_sid']

    @property
    def chat_service_instance_sid(self):
        """
        :returns: The SID of the chat service this user belongs to
        :rtype: unicode
        """
        return self._properties['chat_service_instance_sid']

    @property
    def flex_service_instance_sid(self):
        """
        :returns: The SID of the Flex service instance
        :rtype: unicode
        """
        return self._properties['flex_service_instance_sid']

    @property
    def ui_language(self):
        """
        :returns: The primary language of the Flex UI
        :rtype: unicode
        """
        return self._properties['ui_language']

    @property
    def ui_attributes(self):
        """
        :returns: The object that describes Flex UI characteristics and settings
        :rtype: dict
        """
        return self._properties['ui_attributes']

    @property
    def ui_dependencies(self):
        """
        :returns: The object that defines the NPM packages and versions to be used in Hosted Flex
        :rtype: dict
        """
        return self._properties['ui_dependencies']

    @property
    def ui_version(self):
        """
        :returns: The Pinned UI version
        :rtype: unicode
        """
        return self._properties['ui_version']

    @property
    def service_version(self):
        """
        :returns: The Flex Service version
        :rtype: unicode
        """
        return self._properties['service_version']

    @property
    def call_recording_enabled(self):
        """
        :returns: Whether call recording is enabled
        :rtype: bool
        """
        return self._properties['call_recording_enabled']

    @property
    def call_recording_webhook_url(self):
        """
        :returns: The call recording webhook URL
        :rtype: unicode
        """
        return self._properties['call_recording_webhook_url']

    @property
    def crm_enabled(self):
        """
        :returns: Whether CRM is present for Flex
        :rtype: bool
        """
        return self._properties['crm_enabled']

    @property
    def crm_type(self):
        """
        :returns: The CRM Type
        :rtype: unicode
        """
        return self._properties['crm_type']

    @property
    def crm_callback_url(self):
        """
        :returns: The CRM Callback URL
        :rtype: unicode
        """
        return self._properties['crm_callback_url']

    @property
    def crm_fallback_url(self):
        """
        :returns: The CRM Fallback URL
        :rtype: unicode
        """
        return self._properties['crm_fallback_url']

    @property
    def crm_attributes(self):
        """
        :returns: An object that contains the CRM attributes
        :rtype: dict
        """
        return self._properties['crm_attributes']

    @property
    def public_attributes(self):
        """
        :returns: The list of public attributes
        :rtype: dict
        """
        return self._properties['public_attributes']

    @property
    def plugin_service_enabled(self):
        """
        :returns: Whether the plugin service enabled
        :rtype: bool
        """
        return self._properties['plugin_service_enabled']

    @property
    def plugin_service_attributes(self):
        """
        :returns: The plugin service attributes
        :rtype: dict
        """
        return self._properties['plugin_service_attributes']

    @property
    def integrations(self):
        """
        :returns: A list of objects that contain the configurations for the Integrations supported in this configuration
        :rtype: dict
        """
        return self._properties['integrations']

    @property
    def outbound_call_flows(self):
        """
        :returns: The list of outbound call flows
        :rtype: dict
        """
        return self._properties['outbound_call_flows']

    @property
    def serverless_service_sids(self):
        """
        :returns: The list of serverless service SIDs
        :rtype: unicode
        """
        return self._properties['serverless_service_sids']

    @property
    def wfm_integrations(self):
        """
        :returns: A list of objects that contain the configurations for the WFM Integrations supported in this configuration
        :rtype: dict
        """
        return self._properties['wfm_integrations']

    @property
    def queue_stats_configuration(self):
        """
        :returns: Configurable parameters for Queues Statistics
        :rtype: dict
        """
        return self._properties['queue_stats_configuration']

    @property
    def url(self):
        """
        :returns: The absolute URL of the Configuration resource
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self, ui_version=values.unset):
        """
        Fetch the ConfigurationInstance

        :param unicode ui_version: The Pinned UI version of the Configuration resource to fetch

        :returns: The fetched ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        return self._proxy.fetch(ui_version=ui_version, )

    def create(self):
        """
        Create the ConfigurationInstance

        :returns: The created ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        return self._proxy.create()

    def update(self):
        """
        Update the ConfigurationInstance

        :returns: The updated ConfigurationInstance
        :rtype: twilio.rest.flex_api.v1.configuration.ConfigurationInstance
        """
        return self._proxy.update()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.FlexApi.V1.ConfigurationInstance {}>'.format(context)
