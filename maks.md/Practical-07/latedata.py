from pyflink.common importTypes, WatermarkStrategy, Duration
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.output_tag import OutputTag
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common.time import Time



class EventTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp):
        return value[1]



env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)    # keeps ordering deterministic for the demo


events = [
    ("Picked up", 1000),
    ("At restaurant", 8000),
    ("Order confirmed", 3000),
    ("Delivered", 22000),
    ("Late scan", 2000),    # arrives after watermark passes 10s -> late
]


data = env.from_collection(
    events,
    type_info=Types.TUPLE([Types.STRING(), Types.LONG()])
)


watermarks = (
    WatermarkStrategy
    .for_bounded_out_of_orderness(Duration.of_seconds(2))
    .with_timestamp_assigner(EventTimestampAssigner())
)


stream = data.assign_timestamps_and_watermarks(watermarks)


late_tag = OutputTag(
    "late_events",
    Types.TUPLE([Types.STRING(), Types.LONG()])
)


main = (
    stream
    .key_by(lambda e: "delivery", key_type=Types.STRING())
    .window(TumblingEventTimeWindows.of(Time.seconds(10)))
    .side_output_late_data(late_tag)
    .reduce(
           lambda a, b: a,
           output_type=Types.TUPLE([Types.STRING(), Types.LONG()])
    )
)


late = main.get_side_output(late_tag)
main.print("main")
late.print("late")


env.execute("Food Delivery Late Data")
