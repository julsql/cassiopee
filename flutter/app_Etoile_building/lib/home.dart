import 'package:flutter/material.dart';
import 'package:etoile_project/widgets/nav-drawer.dart';

// Homepage of the project

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    Widget titleSection = const Padding(
      padding: EdgeInsets.all(30),
      child: Text(
        'This application allows to manage the IoT devices contained in the Bâtiment Etoile of the Télécom SudParis and IMT-BS campus.',
        style: TextStyle(
          fontSize: 24.0,
          fontWeight: FontWeight.bold,
        ),
        softWrap: true,
      ),
    );

    Widget textSection = const Padding(
      padding: EdgeInsets.all(30),
      child: Text(
        'To visualize a specific floor of the building, please choose select a floor in the Menu section.',
        style: TextStyle(
          fontSize: 15.0,
        ),
        softWrap: true,
      ),
    );

    return Scaffold(
      drawer: NavDrawer(),
      appBar: AppBar(title: Text("Menu")),
      body: ListView(
        children: [
          Image.asset(
            'images/test_banniere.jpg',
            fit: BoxFit.cover,
          ),
          titleSection,
          textSection,
        ],
      ),
    );
  }
}
