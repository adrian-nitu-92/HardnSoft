package buc1.probulator.buc1.communication;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Observable;
import java.util.Observer;
import java.util.StringTokenizer;

public class Storage extends Observable implements Serializable {
    private ArrayList<Observer> observers;
    private HashMap<String, ArrayList<DataUnit>> store;
    private ReplyParser parser;

    private int numSteps;
    private double numStepsTimestamp;

    private ArrayList<Double> heartRate;
    private ArrayList<Double> heartRateTimestamps;
    private int lastChunkIndex;

    private ArrayList<Double> humidity;
    private ArrayList<Double> humidityTimestamps;
    private int humidityLastChunkIndex;

    private ArrayList<Double> airTemperature;
    private ArrayList<Double> airTemperatureTimestamps;
    private int airTemperatureLastChunkIndex;

    private ArrayList<TreasureInfo> treasures;

    private static Storage storage;

    private Storage() {
        store = new HashMap<>();
        parser = new ReplyParser();
        observers = new ArrayList<>();

        numSteps = 0;
        numStepsTimestamp = 0;

        heartRate = new ArrayList<>();
        heartRateTimestamps = new ArrayList<>();
        lastChunkIndex = 0;

        humidity = new ArrayList<>();
        humidityTimestamps = new ArrayList<>();
        humidityLastChunkIndex = 0;

        airTemperature = new ArrayList<>();
        airTemperatureTimestamps = new ArrayList<>();
        airTemperatureLastChunkIndex = 0;

        treasures = new ArrayList<>();
    }

    public static Storage getInstance(){
        if (storage == null) {
            storage = new Storage();
        }

        return storage;
    }

    public void update(String data) {
        System.out.println("RECEIVED " + data);
        parser.parse(data);

        notifyObservers(null);

        System.out.println("[NUM STEPS] " + getNumSteps());
        System.out.println("[HEARTRATE] " + getHeartRate());
        System.out.println("[HUMIDITY] " + getHeartRate());
        System.out.println("[AIR TEMPERATURE] " + getAirTemperature());
    }

    public int getNumSteps() {
        return numSteps;
    }

    public double getNumStepsTimestamp() {
        return numStepsTimestamp;
    }

    public ArrayList<Double> getHeartRate() {
        return heartRate;
    }

    public ArrayList<Double> getHeartRateTimestamps() {
        return heartRateTimestamps;
    }

    public int getLastChunkIndex() {
        return lastChunkIndex;
    }

    public void incLastChunkIndex() {
        lastChunkIndex++;
    }

    public ArrayList<Double> getHumidity() {
        return humidity;
    }

    public ArrayList<Double> getHumidityTimestamps() {
        return humidityTimestamps;
    }

    public int getHumidityLastChunkIndex() {
        return humidityLastChunkIndex;
    }

    public void incHumidityLastChunkIndex() {
        humidityLastChunkIndex++;
    }

    public ArrayList<Double> getAirTemperature() {
        return airTemperature;
    }

    public ArrayList<Double> getAirTemperatureTimestamps() {
        return airTemperatureTimestamps;
    }

    public int getAirTemperatureLastChunkIndex() {
        return airTemperatureLastChunkIndex;
    }

    public void incAirTemperatureLastChunkIndex() {
        airTemperatureLastChunkIndex++;
    }

    public ArrayList<TreasureInfo> getTreasures() {
        return treasures;
    }

    @Override
    public void notifyObservers(Object arg) {
        for (Observer o : observers) {
            o.update(this, arg);
        }
    }

    @Override
    public void deleteObserver(Observer o) {
        observers.remove(o);
    }

    @Override
    public void addObserver(Observer o) {
        observers.add(o);
    }

    public class TreasureInfo {
        private String name;
        private int checkpoint;
        private double value;
        private double timestamp;

        public TreasureInfo(String name, int checkpoint, double value, double timestamp) {
            this.name = name;
            this.checkpoint = checkpoint;
            this.value = value;
            this.timestamp = timestamp;
        }

        public String getName() {
            return name;
        }

        public int getCheckpoint() {
            return checkpoint;
        }

        public double getValue() {
            return value;
        }

        public double getTimestamp() {
            return timestamp;
        }
    }

    private class ReplyParser {

        private ReplyParser() {
        }

        public void parse(String string) {
            if (string == null || "".equals(string)) {
                return;
            }

            StringTokenizer argsTokenizer = new StringTokenizer(string, ";");

            while (argsTokenizer.hasMoreTokens()) {
                String arg = argsTokenizer.nextToken();

                if (arg== null || "".equals(arg)) {
                    return;
                }

                StringTokenizer argTokenizer = new StringTokenizer(arg, "=");
                String key = argTokenizer.nextToken();

                if (!argTokenizer.hasMoreTokens()) {
                    continue;
                }

                String value = argTokenizer.nextToken();

                if (value == null || "".equals(value)) {
                    continue;
                }

                StringTokenizer valueTokenizer = new StringTokenizer(value, "|");
                ArrayList<DataUnit> values = new ArrayList<>();

                if (key.equals("numsteps")) {
                    String unit = valueTokenizer.nextToken();

                    if (unit == null || "".equals(unit)) {
                        continue;
                    }

                    StringTokenizer unitTokenizer = new StringTokenizer(unit);

                    Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                    String data = unitTokenizer.nextToken();

                    numSteps = (int) Double.parseDouble(data);
                    numStepsTimestamp = timestamp;

                    continue;
                }

                if (key.equals("heartrate")) {
                    while (valueTokenizer.hasMoreTokens()) {
                        String unit = valueTokenizer.nextToken();

                        if (unit == null || "".equals(unit)) {
                            continue;
                        }

                        StringTokenizer unitTokenizer = new StringTokenizer(unit);

                        Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                        String data = unitTokenizer.nextToken();

                        heartRate.add(Double.parseDouble(data));
                        heartRateTimestamps.add(timestamp);

                        continue;
                    }
                }

                if (key.equals("humidity")) {
                    while (valueTokenizer.hasMoreTokens()) {
                        String unit = valueTokenizer.nextToken();

                        if (unit == null || "".equals(unit)) {
                            continue;
                        }

                        StringTokenizer unitTokenizer = new StringTokenizer(unit);

                        Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                        String data = unitTokenizer.nextToken();

                        humidity.add(Double.parseDouble(data));
                        humidityTimestamps.add(timestamp);

                        continue;
                    }
                }

                if (key.equals("airtemperature")) {
                    while (valueTokenizer.hasMoreTokens()) {
                        String unit = valueTokenizer.nextToken();

                        if (unit == null || "".equals(unit)) {
                            continue;
                        }

                        StringTokenizer unitTokenizer = new StringTokenizer(unit);

                        Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                        String data = unitTokenizer.nextToken();

                        airTemperature.add(Double.parseDouble(data));
                        airTemperatureTimestamps.add(timestamp);

                        continue;
                    }
                }

                if (key.equals("treasure")) {
                    while (valueTokenizer.hasMoreTokens()) {
                        String unit = valueTokenizer.nextToken();

                        if (unit == null || "".equals(unit)) {
                            continue;
                        }

                        StringTokenizer unitTokenizer = new StringTokenizer(unit);

                        Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                        int checkpoint = (int) Double.parseDouble(unitTokenizer.nextToken());
                        double dataValue = Double.parseDouble(unitTokenizer.nextToken());
                        String name = unitTokenizer.nextToken();

                        treasures.add(new TreasureInfo(name, checkpoint, dataValue, timestamp));

                        continue;
                    }
                }


            }

        }
    }
}
