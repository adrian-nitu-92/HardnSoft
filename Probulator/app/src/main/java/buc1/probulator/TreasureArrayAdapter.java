package buc1.probulator;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;

import buc1.probulator.buc1.communication.Storage;

public class TreasureArrayAdapter extends ArrayAdapter<Storage.TreasureInfo> {
    private Context context;
    private int resource;
    private ArrayList<Storage.TreasureInfo> content;

    public TreasureArrayAdapter(Context context, int resource, ArrayList<Storage.TreasureInfo> content) {
        super(context, resource, content);
        this.context = context;
        this.resource = resource;
        this.content = content;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View view;
        if (convertView == null) {
            LayoutInflater layoutinflator = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            view = layoutinflator.inflate(resource, null);
        } else {
            view = convertView;
        }

        Storage.TreasureInfo treasure = content.get(position);

        TextView treasureName = (TextView) view.findViewById(R.id.treasure_name);
        TextView treasureValue = (TextView) view.findViewById(R.id.treasure_value);
        TextView treasureCheckpoint = (TextView) view.findViewById(R.id.treasure_checkpoint);

        treasureName.setText(treasure.getName());
        treasureValue.setText(treasure.getValue() + "");
        treasureCheckpoint.setText(treasure.getCheckpoint() + "");

        return view;
    }
}
