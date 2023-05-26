import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:core';

class Floor extends StatefulWidget {
  final int floorNumber;
  const Floor(this.floorNumber);

  @override
  // ignore: no_logic_in_create_state
  State<Floor> createState() => FloorState(floorNumber);
}

class FloorState extends State<Floor> {
  List rooms = [];
  List doors = [];
  List windows = [];
  final int floorNumber;
  FloorState(this.floorNumber);

  String getTitle() {
    if (floorNumber == 1){
      return "First Floor";
    }
    else if (floorNumber == 2){
      return "Second Floor";
    }
    else if (floorNumber == 3){
      return "Third Floor";
    }
    else if (floorNumber == 4){
      return "Fourth Floor";
    }
    return "Ground floor";
  }

  @override
  void initState() {
    super.initState();
    readJson();
  }

  // Fetch content from the json file
  Future<void> readJson() async {
    final String responseRooms = await rootBundle.loadString('json/rooms.json');
    final dataRooms = await json.decode(responseRooms);

    final String responseDoors = await rootBundle.loadString('json/doors.json');
    final dataDoors = await json.decode(responseDoors);

    final String responseWindows = await rootBundle.loadString('json/windows.json');
    final dataWindows = await json.decode(responseWindows);
    setState(() {
      rooms = dataRooms;
      doors = dataDoors;
      windows = dataWindows;
    });
  }

   void drawRectangles(Canvas canvas, Size size, List rectanglePoints, Color color) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final path = Path();
    path.moveTo(rectanglePoints[0][0]*10, rectanglePoints[0][1]*10);

    for (int i = 1; i < rectanglePoints.length; i++) {
      final x = rectanglePoints[i][0]*10;
      final y = rectanglePoints[i][1]*10;
      path.lineTo(x, y);
    }
    

    path.close();

    canvas.drawPath(path, paint);
   }

  bool isFloor(String id){
    RegExp regex = RegExp(r'F(\d+)');
    RegExpMatch? match = regex.firstMatch(id);

    if (match != null) {
      String? digitString = match.group(1);
      int? digit = int.tryParse(digitString!);

      if (digit != null) {
        return digit == floorNumber;
      } else {
        print("Aucun entier trouvé après F.");
      }
    } else {
      print("Aucune correspondance trouvée pour F.");
    }
    return false;
  }

  void drawObjects(Canvas canvas, Size size, List objects, Color color) {
    List<List<List<double>>> objectsFloor = [];
    for (int i=0; i<objects.length; i++) {
      String id = objects[i]["id"];
      if (isFloor(id)) {
        final List<List<double>> object = (objects[i]["relativePosition"]["value"]["coordinates"] as List)
        .map<List<double>>((dynamic point) =>
        (point as List).map<double>((dynamic value) => value.toDouble()).toList()).toList();
        objectsFloor.add(object);
      }
    }

    for (int i=0; i<objectsFloor.length; i++) {
      final List<List<double>> rectanglePoints = objectsFloor[i];
      drawRectangles(canvas, size, rectanglePoints, color);
    }
  }

  void drawFloor(Canvas canvas, Size size, List rooms, List doors, List windows) {
    drawObjects(canvas, size, rooms, Colors.grey);
    drawObjects(canvas, size, doors, Colors.red);
    drawObjects(canvas, size, windows, Colors.blue);
  }

  @override
  Widget build(BuildContext context) {
    final floorState = FloorState(floorNumber);
    String title = getTitle();
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text(title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(25),
        child: Column(
          children: [
            // Display the data loaded from sample.json
            rooms.isNotEmpty && doors.isNotEmpty && windows.isNotEmpty
                ? Expanded(
                    child:  CustomPaint(
                      painter: _MyPainter(floorState, rooms, doors, windows)
                    ),
                )
                : Container(),
          ],
        ),
      ),
    );
  }
}
class _MyPainter extends CustomPainter {

  final List rooms;
  final List doors;
  final List windows;
  final FloorState floorState;

  _MyPainter(this.floorState, this.rooms, this.doors, this.windows);

   @override
   void paint(Canvas canvas, Size size) {
     
     floorState.drawFloor(canvas, size, rooms, doors, windows);
   }

   @override
   bool shouldRepaint(covariant CustomPainter oldDelegate) {
     return false;
   }
}