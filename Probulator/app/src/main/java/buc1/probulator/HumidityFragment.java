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


public class HumidityFragment extends Fragment implements Observer {

    private static HumidityFragment fragment;

    private GraphicalView mChart;

    private XYMultipleSeriesDataset dataset;
    private XYSeriesRenderer visitsRenderer;
    private XYMultipleSeriesRenderer multiRenderer;


    public static HumidityFragment newInstance() {
        if (fragment== null) {
            fragment = new HumidityFragment();
            Bundle args = new Bundle();
            fragment.setArguments(args);
        }
        return fragment;
    }

    public HumidityFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_humidity, container, false);
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
        try {
            mChart.repaint();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        try {
            mChart.repaint();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void update(Observable observable, Object data) {
        if (fragment != null && fragment.isVisible()) {
            try {
                getActivity().runOnUiThread(new Runnable() {
                    public void run() {
                        try {
                            mChart.repaint();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }

                    }
                });
            } catch (Exception e) {
            }
        }
    }

    private void setupChart(){
        dataset = new XYMultipleSeriesDataset();
        dataset.addSeries(Storage.getInstance(getActivity()).getHumiditySeries());

        visitsRenderer = new XYSeriesRenderer();
        visitsRenderer.setColor(Color.BLUE);
        visitsRenderer.setPointStyle(PointStyle.CIRCLE);
        visitsRenderer.setFillPoints(true);
        visitsRenderer.setLineWidth(2);
        visitsRenderer.setDisplayChartValues(true);

        multiRenderer = new XYMultipleSeriesRenderer();
        multiRenderer.setChartTitle("Humidity");
        multiRenderer.setXTitle("Time");
        multiRenderer.setYTitle("Humidity");

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
        multiRenderer.setDisplayChartValues(false);

        LinearLayout chartContainer = (LinearLayout) getActivity().findViewById(R.id.humidity_chart_container);
        mChart = (GraphicalView) ChartFactory.getTimeChartView(getActivity().getBaseContext(), dataset, multiRenderer, "hh:mm:ss");
        chartContainer.addView(mChart);
    }
}
