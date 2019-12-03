#!/bin/bash

TRACE_SUBSYSTEM="/sys/kernel/debug/tracing"

cd $TRACE_SUBSYSTEM

# Start pings
iperf3 -c 192.168.123.206 -u -b 0 --length 512
IPERF_PID=$!

# Clear prev tracer
echo nop > current_tracer
echo 0 > events/enable

echo function_graph > current_tracer
echo ip-* > set_ftrace_filter
echo $IPERF_PID > set_ftrace_pid
echo > trace

#Switch tracing on and off
echo 1 > /sys/kernel/debug/tracing/tracing_on
sleep 2
echo 0 > /sys/kernel/debug/tracing/tracing_on
