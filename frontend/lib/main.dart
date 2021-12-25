import 'package:flutter_neumorphic/flutter_neumorphic.dart';

import './onboarding/onboardingcontrol.dart';
import 'resultscreen/resultscreen.dart';
import 'package:dio/dio.dart';
import 'package:implicitly_animated_reorderable_list/implicitly_animated_reorderable_list.dart';
import './utils/place.dart';

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
        var anotherTempMap = anotherTempArray.asMap();
        var anotherStringyString = anotherTempMap[0];
        var finalAddressArray = anotherStringyString?.split('"');
        var finalTempArray = otherStringyString.split('(');

        newList.add(Place(
            address: finalAddressArray![0],
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
                decoration: InputDecoration(
                  filled: true,
                  hintText: 'Search For A Place You\'ve Been',
                  hintStyle: const TextStyle(
                    color: Color(0xF86BBBDF),
                  ),
                  fillColor: Colors.grey[700],
                  border: const OutlineInputBorder(
                      borderSide: BorderSide(color: Color(0xFF616161)),
                      borderRadius: BorderRadius.all(Radius.circular(10))),
                  focusedBorder: const OutlineInputBorder(
                      borderSide: BorderSide(color: Color(0xFF616161)),
                      borderRadius: BorderRadius.all(Radius.circular(10))),
                  prefixIcon: const Icon(
                    Icons.search,
                    color: Color(0xF86BBBDF),
                  ),
                ),
                style: const TextStyle(
                  color: Color(0xF86BBBDF),
                ),
                // ),
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
      ),
    );
  }

  Widget buildItem(BuildContext context, Place place) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        const SizedBox(
          height: 19,
          child: Divider(
            color: Colors.black,
            thickness: 1,
          ),
        ),
        InkWell(
          child: Padding(
            padding: const EdgeInsets.only(
              bottom: 5,
              top: 5,
            ),
            child: Row(
              children: [
                const SizedBox(
                  width: 36,
                  child: AnimatedSwitcher(
                    duration: Duration(milliseconds: 500),
                    child: Icon(
                      Icons.place,
                      color: Colors.black,
                    ),
                  ),
                ),
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
                                    const TextStyle(color: Color(0xF86BBBDF)),
                                textAlign: TextAlign.left,
                              ),
                              const SizedBox(height: 2),
                              Text(
                                place.address,
                                textAlign: TextAlign.left,
                                style:
                                    const TextStyle(color: Color(0xF86BBBDF)),
                              ),
                            ],
                          )),
                    ],
                  ),
                ),
              ],
            ),
            // ),
          ),
        )
      ],
    );
  }
}
