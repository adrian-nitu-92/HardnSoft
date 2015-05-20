package buc1.probulator.settings;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.RadioGroup;

import java.util.ArrayList;
import java.util.Arrays;

import buc1.probulator.R;

public class RadioButtonListFragment extends SettingsDialogFragment {
    private static final String ARG_TITLE = "title";
    private static final String ARG_LABELS = "labels";
    private static final String ARG_VALUES = "values";

    private Enum valueSelectedButton;
    private ButtonProperties buttonProperties;

    public static RadioButtonListFragment newInstance(int title,
            CharSequence [] labels, Enum [] values) {
        RadioButtonListFragment fragment = new RadioButtonListFragment();

        Bundle args = new Bundle();
        args.putInt(ARG_TITLE, title);
        args.putCharSequenceArray(ARG_LABELS, labels);
        args.putSerializable(ARG_VALUES, values);
        fragment.setArguments(args);

        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        getDialog().setTitle(getArguments().getInt(ARG_TITLE));
        return inflater.inflate(R.layout.fragment_radio_button_list, container, false);
    }

    @Override
    public void onActivityCreated (Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        buttonProperties = new ButtonProperties(
                getArguments().getCharSequenceArray(ARG_LABELS),
                (Enum []) getArguments().getSerializable(ARG_VALUES));

        for (CharSequence label : buttonProperties.labels) {
            addRadioButtonToGroup(label.toString());
        }

        checkRadioButton(valueSelectedButton);
    }

    public Enum getValue() {
        RadioGroup radioGroup = (RadioGroup) getView().findViewById(R.id.radio_group);
        RadioButton button = (RadioButton) getView().findViewById(radioGroup.getCheckedRadioButtonId());

        int buttonIndex = buttonProperties.labels.indexOf(button.getText());
        return buttonProperties.values.get(buttonIndex);
    }

    public void setValue(Enum value) {
        this.valueSelectedButton = value;
    }

    private void checkRadioButton(Enum value) {
        RadioGroup radioGroup = (RadioGroup) getView().findViewById(R.id.radio_group);
        int buttonIndex = buttonProperties.values.indexOf(value);
        RadioButton radioButton = (RadioButton) radioGroup.getChildAt(buttonIndex);
        radioGroup.check(radioButton.getId());
    }

    private void addRadioButtonToGroup(String label) {
        final RadioButtonListFragment fragment = this;

        RadioButton radioButton = (RadioButton) getActivity().getLayoutInflater().inflate(R.layout.radio_button, null);
        radioButton.setText(label);
        radioButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fragment.save();
                fragment.dismiss();
            }
        });

        RadioGroup radioGroup = (RadioGroup) getView().findViewById(R.id.radio_group);
        radioGroup.addView(radioButton);
    }

    private class ButtonProperties {

        private ArrayList<Enum> values;
        private ArrayList<CharSequence> labels;

        public ButtonProperties(CharSequence [] labels, Enum [] values) {
            this.values = new ArrayList<Enum>(Arrays.asList(values));
            this.labels = new ArrayList<CharSequence>(Arrays.asList(labels));
        }
    }
}
