package buc1.probulator.storage;

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;

public class SettingsStorage {

    public static enum Sex {
        MALE, FEMALE;
    }

    private static SettingsStorage instance;
    SharedPreferences.Editor editor;
    SharedPreferences app_preferences;

    public static final String WEIGHT = "weight";
    public static final String HEIGHT = "height";
    public static final String AGE = "age";
    public static final String SEX = "sex";

    public static synchronized SettingsStorage getInstance (Context context) {
        if (instance == null)
            instance = new SettingsStorage(context);
        return instance;
    }

    private SettingsStorage(Context context) {
        app_preferences = PreferenceManager.getDefaultSharedPreferences(context);
        editor = app_preferences.edit();
    }

    public void setWeightKg (Float value) {
        editor.putString(WEIGHT, value.toString());
        editor.commit();
    }

    public Float getWeightKg () {
        String valueStr = app_preferences.getString(WEIGHT, "55f");
        return Float.parseFloat(valueStr);
    }

    public void setHeightCm (Integer value) {
        editor.putString(HEIGHT, value.toString());
        editor.commit();
    }

    public Integer getHeightCm () {
        String valueStr = app_preferences.getString(HEIGHT, "150");
        return Integer.parseInt(valueStr);
    }

    public void setAge (Integer value) {
        editor.putString(AGE, value.toString());
        editor.commit();
    }

    public Integer getAge () {
        String valueStr = app_preferences.getString(AGE, "20");
        return Integer.parseInt(valueStr);
    }

    public void setSex (Sex value) {
        editor.putString(SEX, value.toString());
        editor.commit();
    }

    public Sex getSex () {
        String valueStr = app_preferences.getString(SEX, null);
        if (valueStr == null)
            return Sex.FEMALE;
        return Sex.valueOf(valueStr);
    }
}
