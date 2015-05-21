package buc1.probulator.settings;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.NumberPicker;

import buc1.probulator.R;

public class SinglePickerFragment extends SettingsDialogFragment {

    private static final String ARG_TITLE = "title";
    private int value;

    public static SinglePickerFragment newInstance(int title) {
        SinglePickerFragment fragment = new SinglePickerFragment();

        Bundle args = new Bundle();
        args.putInt(ARG_TITLE, title);
        fragment.setArguments(args);

        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        getDialog().setTitle(getArguments().getInt(ARG_TITLE));
        return inflater.inflate(R.layout.fragment_single_picker, container, false);
    }

    @Override
    public void onActivityCreated (Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        NumberPicker numberPicker = (NumberPicker) getView().findViewById(R.id.number_picker);
        numberPicker.setMaxValue(Integer.MAX_VALUE);
        numberPicker.setValue(value);
        numberPicker.setMinValue(0);
        numberPicker.setWrapSelectorWheel(false);

        final SinglePickerFragment fragment = this;
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

    public void setValue(int value) {
        this.value = value;
    }

    public Integer getValue() {
        NumberPicker numberPicker = (NumberPicker) getView().findViewById(R.id.number_picker);
        return numberPicker.getValue();
    }
}
