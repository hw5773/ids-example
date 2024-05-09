import sys
sys.path.append("..")
from features.flow_psh import FlowPsh
from features.fpkts_per_second import FpktsPerSecond
from features.total_bhlen import TotalBhlen
from features.flow_iat_max import FlowIatMax
from features.backward_packet_length_max import BackwardPacketLengthMax
from features.forward_iat_std import ForwardIatStd
from features.total_length_of_forward_packets import TotalLengthOfForwardPackets
from features.backward_packet_length_std import BackwardPacketLengthStd
from features.forward_iat_min import ForwardIatMin
from features.total_fhlen import TotalFhlen
from features.total_length_of_backward_packets import TotalLengthOfBackwardPackets
from features.total_backward_packets import TotalBackwardPackets
from features.forward_iat_max import ForwardIatMax
from features.forward_packet_length_mean import ForwardPacketLengthMean
from features.backward_iat_min import BackwardIatMin
from features.flow_iat_min import FlowIatMin
from features.backward_packet_length_min import BackwardPacketLengthMin
from features.flow_syn import FlowSyn
from features.bpkts_per_second import BpktsPerSecond
from features.flow_protocol import FlowProtocol
from features.forward_iat_total import ForwardIatTotal
from features.forward_packet_length_min import ForwardPacketLengthMin
from features.backward_iat_max import BackwardIatMax
from features.flow_iat_total import FlowIatTotal
from features.flow_urg import FlowUrg
from features.flow_fin import FlowFin
from features.flow_ece import FlowEce
from features.forward_packet_length_std import ForwardPacketLengthStd
from features.backward_packet_length_mean import BackwardPacketLengthMean
from features.flow_iat_std import FlowIatStd
from features.flow_ack import FlowAck
from features.backward_iat_total import BackwardIatTotal
from features.backward_iat_mean import BackwardIatMean
from features.flow_rst import FlowRst
from features.total_forward_packets import TotalForwardPackets
from features.flow_packets_per_second import FlowPacketsPerSecond
from features.backward_iat_std import BackwardIatStd
from features.flow_cwr import FlowCwr
from features.forward_iat_mean import ForwardIatMean
from features.flow_iat_mean import FlowIatMean
from features.forward_packet_length_max import ForwardPacketLengthMax

def init_features(feature_manager):
    feature_manager.add_feature(FlowPsh("flow_psh"))
    feature_manager.add_feature(FpktsPerSecond("fpkts_per_second"))
    feature_manager.add_feature(TotalBhlen("total_bhlen"))
    feature_manager.add_feature(FlowIatMax("flow_iat_max"))
    feature_manager.add_feature(BackwardPacketLengthMax("backward_packet_length_max"))
    feature_manager.add_feature(ForwardIatStd("forward_iat_std"))
    feature_manager.add_feature(TotalLengthOfForwardPackets("total_length_of_forward_packets"))
    feature_manager.add_feature(BackwardPacketLengthStd("backward_packet_length_std"))
    feature_manager.add_feature(ForwardIatMin("forward_iat_min"))
    feature_manager.add_feature(TotalFhlen("total_fhlen"))
    feature_manager.add_feature(TotalLengthOfBackwardPackets("total_length_of_backward_packets"))
    feature_manager.add_feature(TotalBackwardPackets("total_backward_packets"))
    feature_manager.add_feature(ForwardIatMax("forward_iat_max"))
    feature_manager.add_feature(ForwardPacketLengthMean("forward_packet_length_mean"))
    feature_manager.add_feature(BackwardIatMin("backward_iat_min"))
    feature_manager.add_feature(FlowIatMin("flow_iat_min"))
    feature_manager.add_feature(BackwardPacketLengthMin("backward_packet_length_min"))
    feature_manager.add_feature(FlowSyn("flow_syn"))
    feature_manager.add_feature(BpktsPerSecond("bpkts_per_second"))
    feature_manager.add_feature(FlowProtocol("flow_protocol"))
    feature_manager.add_feature(ForwardIatTotal("forward_iat_total"))
    feature_manager.add_feature(ForwardPacketLengthMin("forward_packet_length_min"))
    feature_manager.add_feature(BackwardIatMax("backward_iat_max"))
    feature_manager.add_feature(FlowIatTotal("flow_iat_total"))
    feature_manager.add_feature(FlowUrg("flow_urg"))
    feature_manager.add_feature(FlowFin("flow_fin"))
    feature_manager.add_feature(FlowEce("flow_ece"))
    feature_manager.add_feature(ForwardPacketLengthStd("forward_packet_length_std"))
    feature_manager.add_feature(BackwardPacketLengthMean("backward_packet_length_mean"))
    feature_manager.add_feature(FlowIatStd("flow_iat_std"))
    feature_manager.add_feature(FlowAck("flow_ack"))
    feature_manager.add_feature(BackwardIatTotal("backward_iat_total"))
    feature_manager.add_feature(BackwardIatMean("backward_iat_mean"))
    feature_manager.add_feature(FlowRst("flow_rst"))
    feature_manager.add_feature(TotalForwardPackets("total_forward_packets"))
    feature_manager.add_feature(FlowPacketsPerSecond("flow_packets_per_second"))
    feature_manager.add_feature(BackwardIatStd("backward_iat_std"))
    feature_manager.add_feature(FlowCwr("flow_cwr"))
    feature_manager.add_feature(ForwardIatMean("forward_iat_mean"))
    feature_manager.add_feature(FlowIatMean("flow_iat_mean"))
    feature_manager.add_feature(ForwardPacketLengthMax("forward_packet_length_max"))
