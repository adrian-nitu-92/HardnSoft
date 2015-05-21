package buc1.probulator.settings;

import android.app.DialogFragment;
import android.content.DialogInterface;

enum State {SAVE, CANCEL};

public class SettingsDialogFragment extends DialogFragment {
    private SettingsOnDismissListener listener;
    private State state = State.CANCEL;

    public void setDismissHandler(SettingsOnDismissListener listener) {
        this.listener = listener;
    }

    @Override
    public void onDismiss(DialogInterface dialog) {
        super.onDismiss(dialog);
        listener.onDismiss(dialog, this);
    }

    public void save() {
        state = State.SAVE;
    }

    public void cancel() {
        state = State.CANCEL;
    }

    public boolean isSave() {
        return state == State.SAVE;
    }

}
