package com.yash.doshi.wheelchairapp.activity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.afollestad.bridge.Bridge;
import com.afollestad.bridge.MultipartForm;
import com.afollestad.bridge.Request;
import com.afollestad.bridge.Response;
import com.yash.doshi.wheelchairapp.R;

import java.util.ArrayList;
import java.util.Locale;

import io.github.controlwear.virtual.joystick.android.JoystickView;


public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity" ;
    public static String BASE_URL = null;

    protected Button SOS_button;
    protected FloatingActionButton speech_FAB;
    protected TextView speech_Text;
    protected JoystickView joystick;

    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        BASE_URL = getResources().getString(R.string.BASE_URL);
        
        SOS_button = (Button)findViewById(R.id.SOS_button);
        speech_FAB = (FloatingActionButton)findViewById(R.id.speech_FAB);
        speech_Text = (TextView)findViewById(R.id.speech_text);
        joystick = (JoystickView)findViewById(R.id.joystick);

        SOS_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Intent.ACTION_DIAL, Uri.fromParts("tel","100",null)));
            }
        });

        speech_FAB.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast toast = Toast.makeText(getApplicationContext(),
                        "keep the button pressed for speech ",
                        Toast.LENGTH_LONG);
                toast.show();

            }
        });

        speech_FAB.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_BUTTON_PRESS){
                    startVoiceInput();
                }
                return false;
            }
        });

        joystick.setOnMoveListener(new JoystickView.OnMoveListener() {
            @Override
            public void onMove(int angle, int strength) {
                String str_angle = String.valueOf(angle);
                String str_strength = String.valueOf(strength);
                movementRequest(str_angle,str_strength);
            }
        });

    }

    private void startVoiceInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Hello, How can I be of assistance?");

        SpeechRecognizer recognizer = SpeechRecognizer.createSpeechRecognizer(getApplicationContext());

        recognizer.setRecognitionListener(new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle params) {
                Toast.makeText(getApplicationContext(),
                        "Listening....",
                        Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onBeginningOfSpeech() {

            }

            @Override
            public void onRmsChanged(float rmsdB) {

            }

            @Override
            public void onBufferReceived(byte[] buffer) {

            }

            @Override
            public void onEndOfSpeech() {

            }

            @Override
            public void onError(int error) {

            }

            @Override
            public void onResults(Bundle results) {

                ArrayList<String> matches = results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);

                //displaying the first match
                if (matches != null){
                    speech_Text.setText(matches.get(0));
                    avonRequest(matches.get(0));
                }else{
                    Toast.makeText(MainActivity.this, "Failed to recognize speech", Toast.LENGTH_LONG).show();
                }

            }

            @Override
            public void onPartialResults(Bundle partialResults) {

            }

            @Override
            public void onEvent(int eventType, Bundle params) {

            }
        });
    }

    private void avonRequest(String sendText){

        String URL = BASE_URL+"/mobile/avon";
        try {
            MultipartForm form = new MultipartForm().add("Text",sendText);
            Request request = Bridge
                    .post(URL)
                    .body(form)
                    .request();

            Response response = request.response();
            if(response.isSuccess() && response.asString().equals("Success")){
                Toast.makeText(MainActivity.this,"Request sent successfully",Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            Log.e(TAG, "avonRequest: "+ e.toString());
            Toast.makeText(MainActivity.this,e.toString(),Toast.LENGTH_LONG).show();
        }

    }

    private void movementRequest(String angle,String strength){

        String URL = BASE_URL+"/mobile/movement";
        try {
            MultipartForm form = new MultipartForm()
                    .add("angle",angle)
                    .add("strength",strength);
            Request request = Bridge
                    .post(URL)
                    .body(form)
                    .request();

            Response response = request.response();
            if(response.isSuccess() && response.asString().equals("Success")){
                Toast.makeText(MainActivity.this,"Request sent successfully",Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            Log.e(TAG, "movementRequest: "+ e.toString());
            Toast.makeText(MainActivity.this,e.toString(),Toast.LENGTH_LONG).show();
        }

    }

}
