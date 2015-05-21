package buc1.probulator.buc1.communication;

import org.achartengine.chart.TimeChart;
import org.achartengine.model.TimeSeries;
import android.app.Notification;
import android.content.Context;
import android.support.v4.app.NotificationCompat;
import android.support.v4.app.NotificationManagerCompat;

import java.io.Serializable;
import java.sql.Time;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Observable;
import java.util.Observer;
import java.util.StringTokenizer;

import buc1.probulator.R;
import buc1.probulator.TreasureFragment;

public class Storage extends Observable implements Serializable {
    private ArrayList<Observer> observers;
    private HashMap<String, ArrayList<DataUnit>> store;
    private ReplyParser parser;

    private int numSteps;
    private double numStepsTimestamp;

    private int distance;
    private double distanceTimestamp;

    private ArrayList<Double> heartRate;
    private ArrayList<Double> heartRateTimestamps;
    private int lastChunkIndex;
    private TimeSeries heartRateSeries;

    private ArrayList<Double> humidity;
    private ArrayList<Double> humidityTimestamps;
    private int humidityLastChunkIndex;
    private TimeSeries humiditySeries;

    private ArrayList<Double> airTemperature;
    private ArrayList<Double> airTemperatureTimestamps;
    private int airTemperatureLastChunkIndex;
    private TimeSeries airTemperatureSeries;

    private ArrayList<Double> bodyTemperature;
    private ArrayList<Double> bodyTemperatureTimestamps;
    private int bodyTemperatureLastChunkIndex;
    private TimeSeries bodyTemperatureSeries;

    private ArrayList<Double> consumption;
    private ArrayList<Double> consumptionTimestamps;
    private int consumptionLastChunkIndex;
    private TimeSeries consumptionSeries;

    private ArrayList<TreasureInfo> treasures;

    private Context context;
    // EXPERIMENTAL NOTIFICATIONS PART
    private int notification_id = 1;
    private final String NOTIFICATION_ID = "notification_id";
    /* These are the classes you use to start the notification */
    private NotificationCompat.Builder notification_builder;
    private NotificationManagerCompat notification_manager;

    private static Storage storage;

    private Storage(Context c) {
        store = new HashMap<>();
        parser = new ReplyParser();
        observers = new ArrayList<>();

        numSteps = 0;
        numStepsTimestamp = 0;

        distance = 0;
        distanceTimestamp = 0;

        heartRate = new ArrayList<>();
        heartRateTimestamps = new ArrayList<>();
        lastChunkIndex = 0;

        humidity = new ArrayList<>();
        humidityTimestamps = new ArrayList<>();
        humidityLastChunkIndex = 0;

        airTemperature = new ArrayList<>();
        airTemperatureTimestamps = new ArrayList<>();
        airTemperatureLastChunkIndex = 0;

        bodyTemperature = new ArrayList<>();
        bodyTemperatureTimestamps = new ArrayList<>();
        bodyTemperatureLastChunkIndex = 0;

        consumption = new ArrayList<>();
        consumptionTimestamps = new ArrayList<>();
        consumptionLastChunkIndex = 0;

        treasures = new ArrayList<>();

        heartRateSeries = new TimeSeries("Heartrate");
        humiditySeries = new TimeSeries("Humidity");
        airTemperatureSeries = new TimeSeries("Air temperature");
        bodyTemperatureSeries = new TimeSeries("Body temperature");
        consumptionSeries = new TimeSeries("Energy consumption");

        context = c;
    }

    public static Storage getInstance(Context c){
        if (storage == null) {
            storage = new Storage(c);
        }

        return storage;
    }

    public void update(String data) {
        System.out.println("RECEIVED " + data);
        parser.parse(data);

        notifyObservers(null);

        System.out.println("[NUM STEPS] " + getNumSteps());
        System.out.println("[HEARTRATE] " + getHeartRate());
        System.out.println("[HUMIDITY] " + getHumidity());
        System.out.println("[AIR TEMPERATURE] " + getAirTemperature());
        System.out.println("[BODY TEMPERATURE] " + getBodyTemperature());
        System.out.println("[CONSUMPTION] " + getConsumption());
    }

    public int getNumSteps() {
        return numSteps;
    }

    public double getNumStepsTimestamp() {
        return numStepsTimestamp;
    }

    public int getDistance() {
        return distance;
    }

    public double getDistanceTimestamp() {
        return distanceTimestamp;
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

    public ArrayList<Double> getBodyTemperature() {
        return bodyTemperature;
    }

    public ArrayList<Double> getBodyTemperatureTimestamps() {
        return bodyTemperatureTimestamps;
    }

    public int getBodyTemperatureLastChunkIndex() {
        return bodyTemperatureLastChunkIndex;
    }

    public void incBodyTemperatureLastChunkIndex() {
        bodyTemperatureLastChunkIndex++;
    }

    public ArrayList<Double> getConsumption() {
        return consumption;
    }

    public ArrayList<Double> getConsumptionTimestamps() {
        return consumptionTimestamps;
    }

    public int getConsumptionLastChunkIndex() {
        return consumptionLastChunkIndex;
    }

    public void incConsumptionLastChunkIndex() {
        consumptionLastChunkIndex++;
    }

    public ArrayList<TreasureInfo> getTreasures() {
        return treasures;
    }


    /* Series */
    public TimeSeries getHeartRateSeries() {
        return heartRateSeries;
    }

    public TimeSeries getHumiditySeries() {
        return  humiditySeries;
    }

    public TimeSeries getAirTemperatureSeries() {
        return airTemperatureSeries;
    }

    public TimeSeries getBodyTemperatureSeries() {
        return bodyTemperatureSeries;
    }

    public TimeSeries getConsumptionSeries() {
        return consumptionSeries;
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
        private String value;
        private double timestamp;

        public TreasureInfo(String name, int checkpoint, String value, double timestamp) {
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

        public String getValue() {
            return value;
        }

        public double getTimestamp() {
            return timestamp;
        }
    }

    private class ReplyParser {

        private ReplyParser() {
        }

        public Calendar parseTimestamp(double timestamp) {
            Calendar c = Calendar.getInstance();
            c.setTime(new Date((long)timestamp));

            return c;
        }

        public synchronized void parse(String string) {
            try {
                if (string == null || "".equals(string)) {
                    return;
                }

                StringTokenizer argsTokenizer = new StringTokenizer(string, ";");

                while (argsTokenizer.hasMoreTokens()) {
                    String arg = argsTokenizer.nextToken();

                    if (arg == null || "".equals(arg)) {
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

                    if (key.equals("distance")) {
                        String unit = valueTokenizer.nextToken();

                        if (unit == null || "".equals(unit)) {
                            continue;
                        }

                        StringTokenizer unitTokenizer = new StringTokenizer(unit);

                        Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                        String data = unitTokenizer.nextToken();

                        distance = (int) Double.parseDouble(data);
                        distanceTimestamp = timestamp;

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
                            synchronized (heartRateSeries) {
                                heartRateSeries.add(new Date(Math.round(timestamp)), Double.parseDouble(data));
                            }

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
                            synchronized (humiditySeries) {
                                humiditySeries.add(new Date(Math.round(timestamp)), Double.parseDouble(data));
                            }

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
                            synchronized (airTemperatureSeries) {
                                airTemperatureSeries.add(new Date(Math.round(timestamp)), Double.parseDouble(data));
                            }

                            continue;
                        }
                    }

                    if (key.equals("bodytemperature")) {
                        while (valueTokenizer.hasMoreTokens()) {
                            String unit = valueTokenizer.nextToken();

                            if (unit == null || "".equals(unit)) {
                                continue;
                            }

                            StringTokenizer unitTokenizer = new StringTokenizer(unit);

                            Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                            String data = unitTokenizer.nextToken();

                            bodyTemperature.add(Double.parseDouble(data));
                            bodyTemperatureTimestamps.add(timestamp);
                            synchronized (bodyTemperatureSeries) {
                                bodyTemperatureSeries.add(new Date(Math.round(timestamp)), Double.parseDouble(data));
                            }

                            continue;
                        }
                    }

                    if (key.equals("consumption")) {
                        while (valueTokenizer.hasMoreTokens()) {
                            String unit = valueTokenizer.nextToken();

                            if (unit == null || "".equals(unit)) {
                                continue;
                            }

                            StringTokenizer unitTokenizer = new StringTokenizer(unit);

                            Double timestamp = Double.parseDouble(unitTokenizer.nextToken());
                            String data = unitTokenizer.nextToken();

                            consumption.add(Double.parseDouble(data));
                            consumptionTimestamps.add(timestamp);
                            synchronized (consumptionSeries) {
                                consumptionSeries.add(new Date(Math.round(timestamp)), Double.parseDouble(data));
                            }

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
                            String dataValue = unitTokenizer.nextToken();
                            String name = unitTokenizer.nextToken();

                            treasures.add(new TreasureInfo(name, checkpoint, dataValue, timestamp));

                            notification_builder = new NotificationCompat.Builder(context)
                                    .setSmallIcon(R.drawable.ic_launcher)
                                    .setContentTitle("Treasure!")
                                    .setContentText("Found " + name + " at checkpoint " + checkpoint + "!")
                                    .setDefaults(Notification.DEFAULT_ALL)
                                    .setAutoCancel(true);

                            notification_manager = NotificationManagerCompat.from(context);
                            notification_manager.notify(notification_id, notification_builder.build());

                            continue;
                        }
                    }
                }
            } catch(Exception e) {
            }
        }
    }
}
