// Practical 6: Flink fraud detection using KeyedProcessFunction.
// Needs the Flink 1.19.x Maven dependencies/pom.xml from your journal.
import java.io.Serializable;
import org.apache.flink.api.common.state.*;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

public class P06Fraud {
    public static class Tx implements Serializable {
        public String id; public double amount; public long time;
        public Tx() {}  // Needed for Flink POJO serialization.
        public Tx(String id, double amount, long time) {
            this.id = id; this.amount = amount; this.time = time;
        }
    }
    public static class Detect extends KeyedProcessFunction<String, Tx, String> {
        private transient ValueState<Tx> previous;
        @Override public void open(Configuration c) {
            previous = getRuntimeContext().getState(
                new ValueStateDescriptor<>("previous", Types.POJO(Tx.class)));
        }
        @Override public void processElement(Tx t, Context ctx, Collector<String> out)
                throws Exception {
            if (t.amount < 10000) return;  // Consider only large transactions.
            Tx old = previous.value();
            if (old != null && t.time >= old.time && t.time - old.time <= 60000)
                out.collect("FRAUD ALERT: " + t.id + " (" + (t.time-old.time)/1000 + "s)");
            previous.update(t);  // Save latest large transaction for this customer.
        }
    }
    public static void main(String[] args) throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.fromData(new Tx("C101", 15000, 10000), new Tx("C101", 20000, 45000),
                     new Tx("C202", 5000, 50000), new Tx("C101", 18000, 90000))
           .keyBy(t -> t.id).process(new Detect()).print();
        env.execute("Fraud Detection");
    }
}
