UniFlex Application Intents
===============================

## Introduction

We see a wide range of applications with different requirements ranging from bulk transfer to control application. While the former requires very high throughput it can tolerate a large packet delay and is also not negatively affected by packet loss. The latter is different as it requires very low latency and guaranteed packet delivery. Another difference is the required low bitrate of just few kbit/s. Hence, in order to be able to optimize the network for specific metrics there is a need for applications to express their needs.

## Description

We follow a proactive and dynamic application informed approach where applications are able to describe their needs, called intents [1], in terms of communications patterns and preferences like type of traffic, bitrate, burstiness and timeliness. Table 1 shows the list of proposed application intents which is based on classification from [1] and are extended to meet our needs, i.e. direction of traffic

<table>
<tr>
<td><b>Intent</b></td>
<td><b>Type</b></td>
<td><b>Value</b></td>
</tr>
<tr>
<td>Direction</td>
<td>Enum</td>
<td>Downlink, uplink, downlink+uplink</td>
</tr>
<tr>
<td>Category</td>
<td>Enum</td>
<td>Query, bulk transfer, control traffic, stream, IoT</td>
</tr>
<tr>
<td>File size</td>
<td>Int</td>
<td>Number of bytes transferred by the application</td>
</tr>
<tr>
<td>Duration</td>
<td>Int</td>
<td>Time between first and last packet in seconds</td>
</tr>
<tr>
<td>Bitrate</td>
<td>Int</td>
<td>Size divided by duration in bytes per second</td>
</tr>
<tr>
<td>Burstiness</td>
<td>Enum</td>
<td>Random bursts, regular bursts, no bursts or bulk (congestion window limited)</td>
</tr>
<tr>
<td>Timeliness</td>
<td>Enum</td>
<td>Stream (low delay, low jitter), interactive (low delay), transfer (completes eventually)</td>
</tr>
<tr>
<td>Resilience</td>
<td>Enum</td>
<td>Sensitive to connection loss, undesirable (loss can be handled) or resilient (loss is tolerable)</td>
</tr>
</table>
Table 1: List of application intents (based on [1]).

## Contact

Anatolij Zubow (zubow@tkn.tu-berlin.de)

## References

[1] Schmidt, P. S., Enghardt, T., Khalili, R., & Feldmann, A. (2013, December). Socket intents: Leveraging application awareness for multi-access connectivity. In Proceedings of the ninth ACM conference on Emerging networking experiments and technologies (pp. 295-300). ACM.
