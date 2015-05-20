package buc1.probulator;

import android.support.v4.app.Fragment;

import android.app.Activity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import java.util.Observable;
import java.util.Observer;

import buc1.probulator.buc1.communication.DataUnit;
import buc1.probulator.buc1.communication.Storage;


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
