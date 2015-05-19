package buc1.probulator;

import android.support.v4.app.Fragment;

import android.app.Activity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import java.util.Observable;
import java.util.Observer;

import buc1.probulator.buc1.communication.Storage;

public class TreasureFragment extends Fragment implements Observer {

    private static TreasureFragment fragment;
    private TreasureArrayAdapter adapter;

    public static TreasureFragment newInstance() {
        if (fragment == null) {
            fragment = new TreasureFragment();
            Bundle args = new Bundle();
            fragment.setArguments(args);
        }

        return fragment;
    }

    public TreasureFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_treasure, container, false);
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        Storage storage = Storage.getInstance();
        adapter = new TreasureArrayAdapter(getActivity(),
                R.layout.layout_treasure_item, storage.getTreasures());

        ListView listView = (ListView) getView().findViewById(R.id.treasure_list);
        listView.setAdapter(adapter);
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
    public void update(Observable observable, Object data) {
        try {
            getActivity().runOnUiThread(new Runnable() {
                public void run() {
                    if (adapter != null) {
                        adapter.notifyDataSetChanged();
                    }
                }
            });
        } catch (Exception e) {
        }
    }
}
