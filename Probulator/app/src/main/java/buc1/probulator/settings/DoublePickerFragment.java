package buc1.probulator.settings;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.NumberPicker;
import android.widget.TextView;

import buc1.probulator.R;

public class DoublePickerFragment extends SettingsDialogFragment {

    private static final String ARG_TITLE = "title";
    private static final String ARG_SEPARATOR = "separator";
    private static final String ARG_MAX_PK1= "max_picker1";
    private static final String ARG_MIN_PK1 = "min_picker1";
    private static final String ARG_MAX_PK2 = "max_picker2";
    private static final String ARG_MIN_PK2 = "min_picker2";

    private int valuePicker1;
    private int valuePicker2;

    public static DoublePickerFragment newInstance(int title, String separator,
                                                   int maxValuePicker1, int minValuePicker1,
                                                   int maxValuePicker2, int minValuePicker2) {
        DoublePickerFragment fragment = new DoublePickerFragment();

        Bundle args = new Bundle();
        args.putInt(ARG_TITLE, title);
        args.putString(ARG_SEPARATOR, separator);
        args.putInt(ARG_MAX_PK1, maxValuePicker1);
        args.putInt(ARG_MIN_PK1, minValuePicker1);
        args.putInt(ARG_MAX_PK2, maxValuePicker2);
        args.putInt(ARG_MIN_PK2, minValuePicker2);
        fragment.setArguments(args);

        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        getDialog().setTitle(getArguments().getInt(ARG_TITLE));
        return inflater.inflate(R.layout.fragment_double_picker, container, false);
    }

    @Override
    public void onActivityCreated (Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        NumberPicker numberPicker1 = (NumberPicker) getView().findViewById(R.id.number_picker1);
        numberPicker1.setMaxValue(getArguments().getInt(ARG_MAX_PK1));
        numberPicker1.setMinValue(getArguments().getInt(ARG_MIN_PK1));
        numberPicker1.setValue(valuePicker1);
        numberPicker1.setWrapSelectorWheel(false);

        TextView separator = (TextView) getView().findViewById(R.id.separator);
        separator.setText(getArguments().getString(ARG_SEPARATOR));

        NumberPicker numberPicker2 = (NumberPicker) getView().findViewById(R.id.number_picker2);
        numberPicker2.setMaxValue(getArguments().getInt(ARG_MAX_PK2));
        numberPicker2.setMinValue(getArguments().getInt(ARG_MIN_PK2));
        numberPicker2.setValue(valuePicker2);
        numberPicker2.setWrapSelectorWheel(false);

        final DoublePickerFragment fragment = this;
        Button okButton = (Button) getView().findViewById(R.id.ok_button);

        okButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fragment.save();
                fragment.dismiss();
            }
        });

        Button cancelButton = (Button) getView().findViewById(R.id.cancel_button);

        cancelButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fragment.cancel();
                fragment.dismiss();
            }
        });
    }

    public Integer getValuePrimary() {
        NumberPicker numberPicker1 = (NumberPicker) getView().findViewById(R.id.number_picker1);
        return numberPicker1.getValue();
    }

    public Integer getValueSecondary() {
        NumberPicker numberPicker2 = (NumberPicker) getView().findViewById(R.id.number_picker2);
        return numberPicker2.getValue();
    }

    public void setValue(int valuePicker1, int valuePicker2) {
        this.valuePicker1 = valuePicker1;
        this.valuePicker2 = valuePicker2;
    }
}
