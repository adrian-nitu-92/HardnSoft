package buc1.probulator;

import android.support.v4.app.Fragment;

import android.app.Activity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Observable;
import java.util.Observer;

import buc1.probulator.buc1.communication.DataUnit;
import buc1.probulator.buc1.communication.Storage;
import buc1.probulator.storage.SettingsStorage;


public class StepsFragment extends Fragment implements Observer {

    private static StepsFragment stepsFragment;

    public static StepsFragment newInstance() {
        if (stepsFragment == null) {
            stepsFragment = new StepsFragment();
            Bundle args = new Bundle();
            stepsFragment.setArguments(args);
        }
        return stepsFragment;
    }

    public StepsFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_steps, container, false);
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        View view = getView();
        ProgressBar progressBar = (ProgressBar) view.findViewById(R.id.progressBar);
        progressBar.setMax(1000);
    }

    @Override
    public void onStart() {
        super.onStart();
        addStepsNumber();
    }

    @Override
    public void onResume() {
        super.onResume();
        addStepsNumber();
    }

    private void addStepsNumber() {
        Storage store = Storage.getInstance(getActivity());
        int numSteps = store.getNumSteps();
        int distance = store.getDistance();

        View view = getView();

        ProgressBar progressBar = (ProgressBar) view.findViewById(R.id.progressBar);
        progressBar.setProgress(numSteps);
        progressBar.setMax(1000);

        TextView steps = (TextView) view.findViewById(R.id.steps_tv);
        steps.setText(numSteps + " steps");

        TextView dist = (TextView) view.findViewById(R.id.distance_val_tv);
        dist.setText(distance + " m");

        SettingsStorage settingsStorage = SettingsStorage.getInstance(stepsFragment.getActivity());
        double nrCals = 0;

        if (settingsStorage.getSex() == SettingsStorage.Sex.FEMALE) {
            nrCals = 65.09 + (9.56 * settingsStorage.getWeightKg()) +
                    (1.84 * settingsStorage.getHeightCm()) -
                    (4.67 * settingsStorage.getAge());
        } else {
            nrCals = 66.47 + (13.75 * settingsStorage.getWeightKg()) +
                    (5 * settingsStorage.getHeightCm()) -
                    (6.75 * settingsStorage.getAge());
        }

        nrCals = 0.4 * nrCals * distance / 1000;

        NumberFormat formatter = new DecimalFormat("#0.00");
        ((TextView) view.findViewById(R.id.calories)).setText(formatter.format(nrCals) + " calories burned");
    }

    @Override
    public void update(Observable observable, Object data) {
        try {
            getActivity().runOnUiThread(new Runnable() {
                public void run() {
                    addStepsNumber();
                }
            });
        } catch (Exception e) {

        }
    }
}
