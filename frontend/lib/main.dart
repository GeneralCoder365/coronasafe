import 'onboardingcontrol.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:implicitly_animated_reorderable_list/implicitly_animated_reorderable_list.dart';
import 'package:fl_chart/fl_chart.dart';

import 'onboarding.dart';

main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const CheckOnboarding(),
      theme: ThemeData(fontFamily: 'Manrope'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  TextEditingController searchController = TextEditingController();
  List<Place> _suggestions = [];

  void populateList(String query) async {
    var listylist = [];
    List<Place> newList = [];

    if (query.isEmpty) {
      _suggestions = newList;
    } else {
      Dio _dio = Dio();
      var queryParameters = {'search_query': query};
      var data = await _dio.get('http://127.0.0.1:5000/getPlaces/',
          queryParameters: queryParameters);

      String fullString = data.toString();

      listylist = fullString.split('","');
      var listyListAccess = listylist.asMap();

      for (int i = 0; i < listyListAccess.length; i++) {
        var transitionString = listyListAccess[i].toString();

        var tempArray = transitionString.split(')');
        var tempArrayMap = tempArray.asMap();

        var otherStringyString = tempArrayMap[0].toString();
        var stringyString = tempArrayMap[1].toString();
        var anotherTempArray = stringyString.split('}');
        var finalTempArray = otherStringyString.split('(');

        newList.add(Place(
            address: anotherTempArray[0],
            name: finalTempArray[1],
            full: transitionString,
            percentage: 0));
      }
      setState(() {
        _suggestions = newList;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.grey[800],
        resizeToAvoidBottomInset: false,
        body: SafeArea(
          child: Center(
            child: Column(
              children: [
                TextField(
                  onSubmitted: (query) {
                    populateList(query);
                  },
                  decoration: const InputDecoration(
                    hintText: 'Search For A Place You\'ve Been',
                    hintStyle: TextStyle(
                      color: Colors.tealAccent,
                    ),
                  ),
                  style: const TextStyle(
                    color: Colors.tealAccent,
                  ),
                ),
                Expanded(
                  child: SizedBox(
                    height: 200.0,
                    child: ImplicitlyAnimatedList<Place>(
                      items: _suggestions,
                      itemBuilder: (context, animation, item, i) {
                        return buildItem(context, item);
                      },
                      areItemsTheSame: (a, b) => a.name == b.name,
                      updateItemBuilder: (context, animation, item) {
                        return buildItem(context, item);
                      },
                    ),
                  ),
                ),
              ],
            ),
          ),
        ));
  }

  Widget buildItem(BuildContext context, Place place) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        InkWell(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                const SizedBox(
                  width: 36,
                  child: AnimatedSwitcher(
                    duration: Duration(milliseconds: 500),
                    child: Icon(Icons.place),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      ElevatedButton(
                          style: ButtonStyle(
                            backgroundColor:
                                MaterialStateProperty.all(Colors.grey[800]),
                            elevation: MaterialStateProperty.all(0),
                          ),
                          onPressed: () {
                            Navigator.of(context).pushReplacement(
                                MaterialPageRoute(
                                    builder: (context) =>
                                        ResultScreen(place: place)));
                          },
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                place.name,
                                style:
                                    const TextStyle(color: Colors.tealAccent),
                                textAlign: TextAlign.left,
                              ),
                              const SizedBox(height: 2),
                              Text(
                                place.address,
                                textAlign: TextAlign.left,
                                style:
                                    const TextStyle(color: Colors.tealAccent),
                              ),
                            ],
                          ))
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class ResultScreen extends StatefulWidget {
  ResultScreen({Key? key, required this.place}) : super(key: key);
  final Place place;

  @override
  State<ResultScreen> createState() => _ResultScreenState(place: place);
}

class _ResultScreenState extends State<ResultScreen> {
  _ResultScreenState({Key? key, required this.place}) : yesString = place.name;
  String yesString;
  final Place place;
  late double percentage;
  String fullString = '';

  void buildBody(String query) async {
    List listylist = [];
    Dio _dio = Dio();

    var queryParameters = {'search_query': query};

    var data = await _dio.get('http://127.0.0.1:5000/getNumbers/',
        queryParameters: queryParameters);
    if (!mounted) return;
    var newString = data.data.toString();

    listylist = newString.split(':');

    fullString = listylist[1].toString();
    var tempArray = fullString.split('}');
    var string = tempArray[0];
    percentage = double.parse(string);
    setState(() {
      place.percentage = percentage;
    });
  }

  Color chooseColors() {
    if (place.percentage > 67) {
      return Colors.redAccent;
    } else if (place.percentage > 33) {
      return Colors.yellowAccent;
    } else {
      return Colors.greenAccent;
    }
  }

  String getChancesName() {
    if (place.percentage > 67) {
      return 'HIGH';
    } else if (place.percentage > 33) {
      return 'MEDIUM';
    } else {
      return 'LOW';
    }
  }

  @override
  Widget build(BuildContext context) {
    buildBody(place.full);
    return Onboarding(
      backgroundColor: Colors.grey[800],
      pages: [
        Pages(
          widget: SafeArea(
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.only(
                      bottom: 5, top: 20, left: 10, right: 50),
                  width: double.infinity,
                  child: Text(
                    place.name,
                    style: const TextStyle(
                      fontSize: 25,
                      fontFamily: 'Manrope',
                      color: Colors.tealAccent,
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(top: 20),
                  child: SizedBox(
                    height: MediaQuery.of(context).size.height / 2,
                    child: const GoogleMap(
                      initialCameraPosition: CameraPosition(
                        target: LatLng(10, -10),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        Pages(
          widget: SafeArea(
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.only(
                      bottom: 5, top: 20, left: 10, right: 50),
                  width: double.infinity,
                  child: const Text(
                    'Chance of Contracting Covid',
                    style: TextStyle(
                      fontSize: 35,
                      fontFamily: 'Manrope',
                      color: Colors.tealAccent,
                    ),
                  ),
                ),
                SizedBox(
                  height: MediaQuery.of(context).size.height / 1.5,
                  child: Card(
                    elevation: 10,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(4)),
                    color: Colors.grey[800],
                    child: _BarChart(place: place),
                  ),
                ),
                Text(
                  getChancesName(),
                  style: TextStyle(
                    fontSize: 50,
                    color: chooseColors(),
                  ),
                )
              ],
            ),
          ),
        ),
        Pages(
          widget: SafeArea(
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.only(
                      bottom: 5, top: 20, left: 10, right: 50),
                  width: double.infinity,
                  child: const Text(
                    'State Graph',
                    style: TextStyle(
                      fontSize: 35,
                      fontFamily: 'Manrope',
                      color: Colors.tealAccent,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        Pages(
          widget: SafeArea(
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.only(
                      bottom: 5, top: 20, left: 10, right: 50),
                  width: double.infinity,
                  child: const Text(
                    'US Heat Map',
                    style: TextStyle(
                      fontSize: 35,
                      fontFamily: 'Manrope',
                      color: Colors.tealAccent,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
    // return Scaffold(
    //     backgroundColor: Colors.grey[800],
    //     body: SafeArea(
    //       child: SingleChildScrollView(
    //         child: ConstrainedBox(
    //           constraints: BoxConstraints(),
    //           child: Column(
    //             children: [
    //               Row(
    //                 children: [
    //                   BackButton(
    //                     color: Colors.tealAccent,
    //                     onPressed: () {
    //                       Navigator.of(context).pushReplacement(
    //                           MaterialPageRoute(
    //                               builder: (context) => const MyHomePage()));
    //                     },
    //                   ),
    //                 ],
    //               ),
    //               Padding(
    //                 padding: EdgeInsets.only(right: 30, left: 30),
    //                 child: Text(
    //                   'Name: ' +
    //                       place.name.toString() +
    //                       '\n' 'Address:' +
    //                       place.address,
    //                   style: const TextStyle(
    //                     color: Colors.tealAccent,
    //                     fontSize: 20,
    //                   ),
    //                 ),
    //               ),
    //               Container(
    //                 height: MediaQuery.of(context).size.height / 1.5,
    //                 child: Card(
    //                   elevation: 10,
    //                   shape: RoundedRectangleBorder(
    //                       borderRadius: BorderRadius.circular(4)),
    //                   color: Colors.grey[800],
    //                   child: _BarChart(place: place),
    //                 ),
    //               ),
    //               Text(
    //                 getChancesName(),
    //                 style: TextStyle(
    //                   fontSize: 50,
    //                   color: chooseColors(),
    //                 ),
    //               )
    //             ],
    //           ),
    //         ),
    //       ),
    //     ));
  }
}

class Place {
  final String name;
  final String address;
  final String full;
  double percentage;
  Place({
    required this.address,
    required this.name,
    required this.full,
    required this.percentage,
  });
}

class _BarChart extends StatelessWidget {
  const _BarChart({Key? key, required this.place}) : super(key: key);
  final Place place;
  @override
  Widget build(BuildContext context) {
    return BarChart(
      BarChartData(
        titlesData: titlesData,
        barGroups: barGroups,
        alignment: BarChartAlignment.spaceAround,
        maxY: 115,
      ),
      swapAnimationDuration: Duration(milliseconds: 600),
    );
  }

  Color chooseColors() {
    if (place.percentage > 67) {
      return Colors.redAccent;
    } else if (place.percentage > 33) {
      return Colors.yellowAccent;
    } else {
      return Colors.greenAccent;
    }
  }

  FlTitlesData get titlesData => FlTitlesData(
        show: true,
        bottomTitles: SideTitles(
          showTitles: true,
          getTextStyles: (context, value) => TextStyle(
            color: chooseColors(),
            fontWeight: FontWeight.bold,
            fontSize: 14,
          ),
          margin: 20,
          getTitles: (double value) {
            switch (value.toInt()) {
              case 0:
                return '%';
              default:
                return 'oh no';
            }
          },
        ),
        leftTitles: SideTitles(showTitles: false),
        topTitles: SideTitles(showTitles: false),
        rightTitles: SideTitles(showTitles: false),
      );

  FlBorderData get borderData => FlBorderData(
        show: false,
      );

  List<BarChartGroupData> get barGroups => [
        BarChartGroupData(
          x: 0,
          barRods: [
            BarChartRodData(
                width: 40,
                borderRadius: BorderRadius.all(Radius.circular(10)),
                y: place.percentage,
                colors: [Colors.greenAccent, Colors.yellow, Colors.redAccent])
          ],
          showingTooltipIndicators: [0],
        ),
      ];
}
