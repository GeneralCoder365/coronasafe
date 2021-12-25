import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'dart:convert';
import 'package:coronasafe/resultscreen/utils/barchart.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/services.dart';
import 'package:coronasafe/onboarding/onboarding.dart';
import 'package:coronasafe/utils/place.dart';

class ResultScreen extends StatefulWidget {
  const ResultScreen({Key? key, required this.place}) : super(key: key);
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

  late WebViewController _controller;

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
  void initState() {
    super.initState();
    buildBody(place.full);
  }

  @override
  Widget build(BuildContext context) {
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
                      color: Color(0xF86BBBDF),
                    ),
                  ),
                ),
                SizedBox(
                  height: MediaQuery.of(context).size.height / 1.4,
                  child: Card(
                    elevation: 10,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(4)),
                    color: Colors.grey[800],
                    child: MyBarChart(place: place),
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
                      color: Color(0xF86BBBDF),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        Pages(
          widget: Expanded(
            child: SafeArea(
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
                        color: Color(0xF86BBBDF),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: MediaQuery.of(context).size.height / 2,
                    child: WebView(
                      initialUrl: 'about:blank',
                      javascriptMode: JavascriptMode.unrestricted,
                      gestureNavigationEnabled: true,
                      onWebViewCreated: (WebViewController webViewController) {
                        _controller = webViewController;
                        _loadHtmlFromAssets();
                      },
                      gestureRecognizers: <
                          Factory<OneSequenceGestureRecognizer>>{
                        // 2
                        Factory<VerticalDragGestureRecognizer>(
                            () => VerticalDragGestureRecognizer()),
                        Factory<HorizontalDragGestureRecognizer>(
                            () => HorizontalDragGestureRecognizer()),
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  _loadHtmlFromAssets() async {
    String fileText = await rootBundle.loadString('assets/temp-plot.html');
    _controller.loadUrl(Uri.dataFromString(fileText,
            mimeType: 'text/html', encoding: Encoding.getByName('utf-8'))
        .toString());
  }
}
