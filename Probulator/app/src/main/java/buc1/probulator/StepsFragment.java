package buc1.probulator;

import android.support.v4.app.Fragment;

import android.app.Activity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
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
        TextView label = (TextView) view.findViewById(R.id.steps_number_label);
        TextView value = (TextView) view.findViewById(R.id.steps_number_value);

        label.setText("Number of steps");
        value.setText("0");
    }

    private void addStepsNumber() {
        Storage store = Storage.getInstance();
        int numSteps = store.getNumSteps();

        View view = getView();
        TextView label = (TextView) view.findViewById(R.id.steps_number_label);
        TextView value = (TextView) view.findViewById(R.id.steps_number_value);

        label.setText("Number of steps");
        System.out.println("Displaying steps " + numSteps);
        value.setText(numSteps + "");
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
