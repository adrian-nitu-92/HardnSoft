package buc1.probulator;

import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.widget.DrawerLayout;
import android.os.Bundle;
import android.view.Menu;

import buc1.probulator.buc1.communication.Storage;
import buc1.probulator.buc1.communication.Updater;
import buc1.probulator.settings.SettingsFragment;

public class MainActivity extends ActionBarActivity
        implements NavigationDrawerFragment.NavigationDrawerCallbacks {

    /**
     * Fragment managing the behaviors, interactions and presentation of the navigation drawer.
     */
    private NavigationDrawerFragment mNavigationDrawerFragment;

    /**
     * Used to store the last screen title. For use in {@link #restoreActionBar()}.
     */
    private CharSequence mTitle;

    private StepsFragment stepsFragment;
    private HeartRateFragment heartRateFragment;
    private HumidityFragment humidityFragment;
    private AirTemperatureFragment airTemperatureFragment;
    private BodyTemperatureFragment bodyTemperatureFragment;
    private TreasureFragment treasureFragment;
    private ConsumptionFragment consumptionFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mNavigationDrawerFragment = (NavigationDrawerFragment)
                getSupportFragmentManager().findFragmentById(R.id.navigation_drawer);
        mTitle = getTitle();

        mNavigationDrawerFragment.setUp (
                R.id.navigation_drawer,
                (DrawerLayout) findViewById(R.id.drawer_layout));

        Storage storage = Storage.getInstance();
        new Updater(storage).start();

        stepsFragment = StepsFragment.newInstance();
        storage.addObserver(stepsFragment);

        heartRateFragment = HeartRateFragment.newInstance();
        storage.addObserver(heartRateFragment);

        humidityFragment = HumidityFragment.newInstance();
        storage.addObserver(humidityFragment);

        airTemperatureFragment = AirTemperatureFragment.newInstance();
        storage.addObserver(airTemperatureFragment);

        bodyTemperatureFragment =  BodyTemperatureFragment.newInstance();
        storage.addObserver(bodyTemperatureFragment);

        treasureFragment = TreasureFragment.newInstance();
        storage.addObserver(treasureFragment);

        consumptionFragment = ConsumptionFragment.newInstance();
        storage.addObserver(consumptionFragment);
    }

    @Override
    public void onNavigationDrawerItemSelected(int position) {

        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction transaction = fragmentManager.beginTransaction();

        switch (position) {
            case 0:
                transaction.replace(R.id.container, StepsFragment.newInstance());
                break;
            case 1:
                transaction.replace(R.id.container, HeartRateFragment.newInstance());
                break;
            case 2:
                transaction.replace(R.id.container, HumidityFragment.newInstance());
                break;
            case 3:
                transaction.replace(R.id.container, AirTemperatureFragment.newInstance());
                break;
            case 4:
                transaction.replace(R.id.container, BodyTemperatureFragment.newInstance());
                break;
            case 5:
                transaction.replace(R.id.container, ConsumptionFragment.newInstance());
                break;
            case 6:
                transaction.replace(R.id.container, TreasureFragment.newInstance());
                break;
            case 7:
                transaction.replace(R.id.container, new SettingsFragment());
                break;
        }
        transaction.commit();
    }

    public void setTitle(String title) {
        mTitle = title;
    }

    public void restoreActionBar() {
        ActionBar actionBar = getSupportActionBar();
        actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_STANDARD);
        actionBar.setDisplayShowTitleEnabled(true);
        actionBar.setTitle(mTitle);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        if (!mNavigationDrawerFragment.isDrawerOpen()) {
            getMenuInflater().inflate(R.menu.main, menu);
            restoreActionBar();
            return true;
        }
        return super.onCreateOptionsMenu(menu);
    }
}