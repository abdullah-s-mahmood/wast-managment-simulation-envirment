// Independently written installation/linkage probe, not a scientific model.
// Expected event time is exactly 1 ns; no packet/network/traffic model is used.
#include "ns3/nstime.h"
#include "ns3/simulator.h"

#include <iostream>
#include <string_view>

int main(int argc, char** argv)
{
    // Deliberate negative probe for command-status propagation, before any event.
    if (argc == 2 && std::string_view(argv[1]) == "--negative-exit")
    {
        return 7;
    }
    if (argc != 1)
    {
        return 2;
    }
    ns3::Time::SetResolution(ns3::Time::NS);
    long long observed_ns = -1;
    ns3::Simulator::Schedule(ns3::NanoSeconds(1), [&observed_ns]() {
        observed_ns = ns3::Simulator::Now().GetNanoSeconds();
    });
    ns3::Simulator::Run();
    ns3::Simulator::Destroy();
    if (observed_ns != 1)
    {
        return 3;
    }
    std::cout << "{\"status\":\"NS3_CORE_SMOKE_PASS\",\"event_time_ns\":1}\n";
    return 0;
}
