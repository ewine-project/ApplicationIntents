import logging

from sbi.common.events import AppIntentEvent
from sbi.common.intents import Category
from uniflex.core import modules
from uniflex.core import events


__author__ = "Anatolij Zubow"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "{zubow}@tkn.tu-berlin.de"

class QueueParams():
    def __init__(self, aifs, cwmin, cwmax, txop):
        self.aifs = aifs
        self.cwmin = cwmin
        self.cwmax = cwmax
        self.txop = txop

    def getAifs(self):
        return self.aifs

    def getCwMin(self):
        return self.cwmin

    def getCwMax(self):
        return self.cwmax

    def getTxOp(self):
        return self.txop

'''
    Application intents app for IEEE 802.11 technology.
'''

class ApplicationIntentsModule(modules.ControlApplication):
    def __init__(self):
        super(ApplicationIntentsModule, self).__init__()
        self.log = logging.getLogger('app_intents_module.main')
        self.nodes = {} # list of detected network nodes: uuid->node-obj

    @modules.on_start()
    def start_ho_module(self):
        self.log.debug("Start AppIntents module".format())

    @modules.on_exit()
    def stop_ho_module(self):
        self.log.debug("Stop AppIntents module".format())

    @modules.on_event(events.NewNodeEvent)
    def add_node(self, event):
        node = event.node

        self.log.info("Added new node: {}, Local: {}"
                      .format(node.uuid, node.local))
        self.nodes[node.uuid] = node


    @modules.on_event(events.NodeExitEvent)
    @modules.on_event(events.NodeLostEvent)
    def remove_node(self, event):
        self.log.info("Node lost".format())
        node = event.node
        reason = event.reason
        if node.uuid in self.nodes:
            del self.nodes[node.uuid]
            self.log.info("Node: {}, Local: {} removed reason: {}"
                          .format(node.uuid, node.local, reason))


    @modules.on_event(AppIntentEvent)
    def handle_app_intent(self, event):
        """
        Handling an application intent

        :param event: the event contains all required information to adapt to application intents.
        """
        try:
            # TBD: ignore remote events

            # get intent description
            app_intent_desc = event.app_intent_desc

            self.log.info("handle app intent ")

            # just tests
            RATECONTROL_THROUGHPUT = 1
            RATECONTROL_ROBUST = 2
            MPTCP_MULTI_SUBFLOWS = 1
            MPTCP_DIVERSITY_SUBFLOWS = 2

            # TBD ...
            device = event.srcNode.get_device(0)
            #trans_protocol = event.srcNode.get_protocol_by_name('TCP')

            ''' Adapt protocol layers according to intent '''
            if app_intent_desc.category == Category.BULK_TRANSFER:
                ''' PHY layer adaptation '''
                # use aggressiv rate control
                device.set_rate_control(RATECONTROL_THROUGHPUT)

                ''' MAC layer adaptation '''
                # optimize for efficiency
                qp = QueueParams(20, 64, 1024, 5)
                device.set_mac_access_parameters(1, qp)

                ''' Transport layer - see paper An enhanced socket API for Multipath TCP, Hesmans '''
                # use multipath tcp: use multiple flows for multiplexing
                #trans_protocol.set_subflow_mgmt(MPTCP_MULTI_SUBFLOWS)

            elif app_intent_desc.category == Category.CONTROL_TRAFFIC:
                ''' PHY layer adaptation '''
                # use robust or at least not aggressiv rate control
                device.set_rate_control(RATECONTROL_ROBUST)

                ''' MAC layer adaptation '''
                # control traffic use high prio for channel access; as traffic is hopefully of low load collisions
                # should not be a problem
                qp = QueueParams(10, 8, 1024, 0)
                device.set_mac_access_parameters(1, qp)

                ''' Transport layer - see paper An enhanced socket API for Multipath TCP, Hesmans '''
                # use multipath tcp: use multiple flows for path diversity (reliability), i.e. fighting packet loss
                #trans_protocol.set_subflow_mgmt(MPTCP_DIVERSITY_SUBFLOWS)
            else:
                # just default
                pass

        except Exception as e:
            self.log.fatal("set app intents failed: err_msg: %s" % (str(e)))
