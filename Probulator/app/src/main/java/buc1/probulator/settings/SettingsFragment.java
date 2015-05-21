package buc1.probulator.settings;

import android.app.Activity;
import android.app.FragmentManager;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RelativeLayout;
import android.widget.TextView;

import buc1.probulator.R;
import buc1.probulator.storage.SettingsStorage;
import buc1.probulator.MainActivity;

public class SettingsFragment extends Fragment {

    private static final String TITLE = "Settings";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_settings, container, false);
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
    }

    @Override
    public void onActivityCreated (Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        View view = getView();
        FragmentManager manager = getActivity().getFragmentManager();


        RelativeLayout weightField = (RelativeLayout) view.findViewById(R.id.weight_field);
        weightField.setOnClickListener(new FieldListener(SettingsStorage.WEIGHT, manager,
                DoublePickerFragment.newInstance(R.string.weight, ".", 200, 0, 99, 0)));

        RelativeLayout heightField = (RelativeLayout) view.findViewById(R.id.height_field);
        heightField.setOnClickListener(new FieldListener(SettingsStorage.HEIGHT, manager,
                SinglePickerFragment.newInstance(R.string.height)));

        RelativeLayout ageField = (RelativeLayout) view.findViewById(R.id.age_field);
        ageField.setOnClickListener(new FieldListener(SettingsStorage.AGE, manager,
                SinglePickerFragment.newInstance(R.string.age)));

        RelativeLayout sexField = (RelativeLayout) view.findViewById(R.id.sex_field);
        sexField.setOnClickListener(new FieldListener(SettingsStorage.SEX, manager,
                RadioButtonListFragment.newInstance(R.string.sex,
                        new CharSequence [] {"Female", "Male"},
                        new Enum [] {SettingsStorage.Sex.FEMALE, SettingsStorage.Sex.MALE})));

        refreshSettings();
    }

    private void refreshSettings() {
        SettingsStorage settingsStorage = SettingsStorage.getInstance(getActivity());
        displaySettings(R.id.weight_value, settingsStorage.getWeightKg() + " kg");
        displaySettings(R.id.height_value, settingsStorage.getHeightCm() + " cm");
        displaySettings(R.id.age_value, settingsStorage.getAge() + " years" );
        displaySettings(R.id.sex_value, (settingsStorage.getSex().equals(SettingsStorage.Sex.FEMALE)) ? "F" : "M");
    }

    private void displaySettings(int id, String text) {
        TextView textView = (TextView) getView().findViewById(id);
        textView.setText(text);
    }

    private class FieldListener implements View.OnClickListener {

        private String type;
        private FragmentManager fm;
        private SettingsDialogFragment dialogFragment;


        public FieldListener(String type, FragmentManager fm, SettingsDialogFragment dialogFragment) {
            this.fm = fm;
            this.type = type;
            this.dialogFragment = dialogFragment;
        }

        @Override
        public void onClick(View v) {

            SettingsStorage settingsStorage = SettingsStorage.getInstance(dialogFragment.getActivity());
            if (dialogFragment instanceof SinglePickerFragment) {

                SinglePickerFragment singlePicker = (SinglePickerFragment) dialogFragment;
                int value = 0;
                switch (type) {
                    case SettingsStorage.HEIGHT:
                        value = settingsStorage.getHeightCm();
                        break;
                    case SettingsStorage.AGE:
                        value = settingsStorage.getAge();
                        break;
                }
                singlePicker.setValue(value);

            } else if (dialogFragment instanceof DoublePickerFragment) {

                DoublePickerFragment doublePicker = (DoublePickerFragment) dialogFragment;
                switch (type) {
                    case SettingsStorage.WEIGHT:
                        Float floatValue = settingsStorage.getWeightKg();
                        int valuePicker1 = (int) Math.floor(floatValue.doubleValue());
                        int valuePicker2 = (int) ((floatValue - valuePicker1) * 100);
                        doublePicker.setValue(valuePicker1, valuePicker2);
                        break;
                }
            } else if (dialogFragment instanceof RadioButtonListFragment) {
                RadioButtonListFragment radioButtonListFragment = (RadioButtonListFragment) dialogFragment;
                switch (type) {
                    case SettingsStorage.SEX:
                        SettingsStorage.Sex value = settingsStorage.getSex();
                        radioButtonListFragment.setValue(value);
                }
            }

            dialogFragment.setDismissHandler(new SettingsFieldOnDismissListener(type, dialogFragment.getActivity()));
            dialogFragment.show(fm, this.getClass().toString());
        }
    }

    private class SettingsFieldOnDismissListener implements SettingsOnDismissListener {

        private String type;
        private Context context;

        public SettingsFieldOnDismissListener (String type, Context context) {
            this.type = type;
            this.context = context;
        }

        @Override
        public void onDismiss(DialogInterface dialog, SettingsDialogFragment fragment) {

            if (!fragment.isSave()) {
                refreshSettings();
                return;
            }

            SettingsStorage settingsStorage = SettingsStorage.getInstance(context);
            if (fragment instanceof SinglePickerFragment) {

                SinglePickerFragment singlePicker = (SinglePickerFragment) fragment;
                Integer value = singlePicker.getValue();
                switch (type) {
                    case SettingsStorage.HEIGHT:
                        settingsStorage.setHeightCm(value);
                        break;
                    case SettingsStorage.AGE:
                        settingsStorage.setAge(value);
                        break;
                }

            } else if (fragment instanceof DoublePickerFragment) {

                DoublePickerFragment doublePicker = (DoublePickerFragment) fragment;
                switch (type) {
                    case SettingsStorage.WEIGHT:
                        float value = Float.parseFloat(doublePicker.getValuePrimary() +
                                "." + doublePicker.getValueSecondary());
                        settingsStorage.setWeightKg(value);
                        break;
                }
            } else if (fragment instanceof RadioButtonListFragment) {
                RadioButtonListFragment radioButtonListFragment = (RadioButtonListFragment) fragment;
                switch(type) {
                    case SettingsStorage.SEX:
                        SettingsStorage.Sex value = (SettingsStorage.Sex)
                                radioButtonListFragment.getValue();
                        settingsStorage.setSex(value);
                        break;
                }
            }

            refreshSettings();
        }
    }
}
