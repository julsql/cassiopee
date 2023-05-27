import 'package:flutter/material.dart';
import 'package:flutter_cube/flutter_cube.dart';


class TriDim extends StatefulWidget {
  final int floorNumber;
  const TriDim(this.floorNumber);
  @override
  TriDimState createState() => TriDimState(floorNumber);
}

class TriDimState extends State<TriDim> with SingleTickerProviderStateMixin {
  final int floorNumber;
  TriDimState(this.floorNumber);
  Object? _display;
  static const double coef = 50.0;
  Vector3 scale = Vector3(coef, coef, coef);

  void _onSceneCreated(Scene scene) {
    scene.camera.position.z = 40;
    
    _display = Object(scale: scale, backfaceCulling: false, fileName: 'obj/floor_${floorNumber}_rooms.obj');
    Object doors = Object(backfaceCulling: false, fileName: 'obj/floor_${floorNumber}_doors.obj');
    Object windows = Object(backfaceCulling: false, fileName: 'obj/floor_${floorNumber}_windows.obj');
  
    //_cube!.add(_cube2);
    _display!.add(doors);
    _display!.add(windows);
    
    scene.world.add(_display!);
  }

  @override
  void initState() {
    super.initState();
  }

    String getTitle() {
    if (floorNumber == 1){
      return "3D First Floor";
    }
    else if (floorNumber == 2){
      return "3D Second Floor";
    }
    else if (floorNumber == 3){
      return "3D Third Floor";
    }
    else if (floorNumber == 4){
      return "3D Fourth Floor";
    }
    return "3D Ground floor";
  }

  @override
  Widget build(BuildContext context) {
    String title = getTitle();
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: Center(
        child: Cube(
          onSceneCreated: _onSceneCreated,
        ),
      ),
    );
  }
}