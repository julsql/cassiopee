import 'package:flutter/material.dart';
import '../main.dart';
import '../home.dart';
import '../firstfloor.dart';
import '../about.dart';

class NavDrawer extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          ListTile(
            leading: Icon(Icons.input),
            title: Text('Welcome page'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const HomePage()),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('First floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const FirstFloor()),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.info),
            title: Text('About us'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const AboutUs()),
              ),
            },
          ),
        ],
      ),
    );
  }
}
