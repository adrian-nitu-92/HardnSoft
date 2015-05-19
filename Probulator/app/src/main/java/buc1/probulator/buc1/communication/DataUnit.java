package buc1.probulator.buc1.communication;

public class DataUnit {
    double timestamp;
    String values;

    public DataUnit(double timestamp, String values) {
        this.timestamp = timestamp;
        this.values = values;
    }

    public String getValues() {
        return values;
    }

    public String toString() {
        return "(" + timestamp + " " + values + ")";
    }
}
