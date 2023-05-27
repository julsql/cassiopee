import 'package:flutter/material.dart';
import '../home.dart';
import '../about.dart';
import '../floor.dart';
import '../floor_3d.dart';

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
            title: Text('Ground floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(0)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('First floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(1)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('Second floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(2)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('Third floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(3)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('Fourth floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const Floor(4)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('3D First floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => TriDim(1)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('3D Second floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => TriDim(2)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('3D Third floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => TriDim(3)),
              ),
            },
          ),
          ListTile(
            leading: Icon(Icons.home_filled),
            title: Text('3D Fourth floor of the Etoile building'),
            onTap: () => {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => TriDim(4)),
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
