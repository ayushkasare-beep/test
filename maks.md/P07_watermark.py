# Practical 7: Flink watermark, 10-second windows and side output for late events.
# Requires: pip install apache-flink and a compatible Java runtime.
from pyflink.common import Types, WatermarkStrategy, Duration
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.output_tag import OutputTag
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common.time import Time

class EventTime(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp):
        return value[1]

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
events = [("Picked up",1000), ("At restaurant",8000),
          ("Delivered",22000), ("Late scan",2000)]
data = env.from_collection(events, type_info=Types.TUPLE([Types.STRING(),Types.LONG()]))
wm = WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_seconds(2))
stream = data.assign_timestamps_and_watermarks(wm.with_timestamp_assigner(EventTime()))
late_tag = OutputTag("late", Types.TUPLE([Types.STRING(),Types.LONG()]))
main = (stream.key_by(lambda e:"delivery",key_type=Types.STRING())
        .window(TumblingEventTimeWindows.of(Time.seconds(10)))
        .side_output_late_data(late_tag)
        .reduce(lambda a,b:a, output_type=Types.TUPLE([Types.STRING(),Types.LONG()])))
main.print("main")
main.get_side_output(late_tag).print("late")
env.execute("Watermark Demo")
# In very small/batched inputs, late side-output behavior can depend on watermark timing.
