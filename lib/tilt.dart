import 'globals.dart';
import 'dart:async';
import 'package:flutter/material.dart';
import 'config.dart';
import 'package:sensors/sensors.dart';
void tilt(){
  final subscription = accelerometerEvents.listen((AccelerometerEvent event) {
    gcurr = event.y;
  });
}
double min(double a,double b){
  if(a>b){
    return b;
  }else{
    return a;
  }
}
void tsend(){
  if(gcurr>0.4){
    String s = min(gcurr/10,1).toString();
    sock.write("tilt&+&"+s+'%');
  }else if(gcurr<-0.4){
    String s =  min((-1*gcurr)/10,1).toString();
    sock.write("tilt&-&"+s+'%');
  }else{
    sock.write("tilt&+&"+'0'+'%');
  } 
}
class Gyro extends StatefulWidget{
  @override
  _GyroState createState() => _GyroState();
}
class _GyroState extends State<Gyro> {
  @override
  Widget build(BuildContext context){
    if(!ovisit){
      tilt();
      Timer.periodic(Duration(milliseconds:50),(Timer t){
        if(tiltcontrol){
          tsend();
        }
      });
      ovisit=true;
    }
    return Scaffold(
      appBar: AppBar(
        title: Text("Tilt to Control"),
      ),
      body: Center( 
        child : Checkbox(
        value: tiltcontrol,
        onChanged: (bool value) {
          if(!value){
            sock.write("tilt&0%");
          }
          setState(() {
            tiltcontrol=value;
          });
        },
        )
      )
    );
  }
}