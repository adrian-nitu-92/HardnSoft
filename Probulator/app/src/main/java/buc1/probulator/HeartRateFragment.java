package buc1.probulator;

import android.graphics.Paint;
import android.support.v4.app.Fragment;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;

import java.util.ArrayList;
import java.util.Date;
import java.util.Observable;
import java.util.Observer;

import org.achartengine.ChartFactory;
import org.achartengine.GraphicalView;
import org.achartengine.chart.PointStyle;
import org.achartengine.model.TimeSeries;
import org.achartengine.model.XYMultipleSeriesDataset;
import org.achartengine.model.XYSeries;
import org.achartengine.renderer.XYMultipleSeriesRenderer;
import org.achartengine.renderer.XYSeriesRenderer;

import buc1.probulator.buc1.communication.Storage;


public class HeartRateFragment extends Fragment implements Observer {

    private static HeartRateFragment fragment;

    private GraphicalView mChart;

    private XYSeries visitsSeries ;
    private XYMultipleSeriesDataset dataset;

    private XYSeriesRenderer visitsRenderer;
    private XYMultipleSeriesRenderer multiRenderer;


    public static HeartRateFragment newInstance() {
        if (fragment== null) {
            fragment = new HeartRateFragment();
            Bundle args = new Bundle();
            fragment.setArguments(args);
        }
        return fragment;
    }

    public HeartRateFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_heart_rate, container, false);
    }

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
        setupChart();
    }

    @Override
    public void onStart() {
        super.onStart();
        addAllValues();
    }

    private void appendDataToGraph() {
        final Storage storage = Storage.getInstance();
        final ArrayList<Double> y = storage.getHeartRate();
        final ArrayList<Double> x = storage.getHeartRateTimestamps();
        final int lci = storage.getLastChunkIndex();

        Thread t = new Thread() {
            public void run() {
                for (int i = lci; i < x.size(); i++) {
                    storage.incLastChunkIndex();
                    visitsSeries.add(x.get(i), y.get(i));
                }
            }
        };
        t.start();

        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        mChart.repaint();
    }

    @Override
    public void update(Observable observable, Object data) {
        if (fragment != null && fragment.isVisible()) {
            try {
                getActivity().runOnUiThread(new Runnable() {
                    public void run() {
                        appendDataToGraph();
                    }
                });
            } catch (Exception e) {

            }
        }
    }

    private void setupChart(){
        visitsSeries = new XYSeries("Heartrate");

        dataset = new XYMultipleSeriesDataset();
        dataset.addSeries(visitsSeries);

        visitsRenderer = new XYSeriesRenderer();
        visitsRenderer.setColor(Color.RED);
        visitsRenderer.setPointStyle(PointStyle.CIRCLE);
        visitsRenderer.setFillPoints(true);
        visitsRenderer.setLineWidth(2);
        visitsRenderer.setDisplayChartValues(true);

        multiRenderer = new XYMultipleSeriesRenderer();
        multiRenderer.setChartTitle("HeartRate");
        multiRenderer.setXTitle("Time");
        multiRenderer.setYTitle("Heartrate");

        multiRenderer.setChartTitleTextSize(50);
        multiRenderer.setLegendTextSize(10);
        multiRenderer.setLabelsTextSize(15);
        multiRenderer.setAxisTitleTextSize(20);

        multiRenderer.setLabelsColor(Color.BLACK);
        multiRenderer.setXLabelsColor(Color.BLACK);
        multiRenderer.setYLabelsColor(0, Color.BLACK);
        multiRenderer.setMarginsColor(Color.WHITE);
        multiRenderer.setGridColor(Color.GRAY);

        multiRenderer.setYLabelsAlign(Paint.Align.LEFT);
        multiRenderer.setZoomButtonsVisible(false);
        multiRenderer.setPanEnabled(true, true);
        multiRenderer.setAntialiasing(true);

        multiRenderer.setFitLegend(false);
        multiRenderer.setShowLegend(false);

        multiRenderer.setShowGridY(true);
        multiRenderer.setShowGridX(true);
        multiRenderer.setInScroll(true);

        multiRenderer.addSeriesRenderer(visitsRenderer);

        LinearLayout chartContainer = (LinearLayout) getActivity().findViewById(R.id.chart_container);
        mChart = (GraphicalView) ChartFactory.getLineChartView(getActivity().getBaseContext(), dataset, multiRenderer);
        chartContainer.addView(mChart);
    }

    public void addAllValues() {
        final Storage storage = Storage.getInstance();
        final ArrayList<Double> y = storage.getHeartRate();
        final ArrayList<Double> x = storage.getHeartRateTimestamps();
        final int lci = storage.getLastChunkIndex();
        int start = lci < 40? 0 : lci - 40;

        Thread t = new Thread() {
            public void run() {
                for (int i = 0; i < lci; i++) {
                    visitsSeries.add(x.get(i), y.get(i));
                }
            }
        };
        t.start();

        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        mChart.repaint();
    }
}