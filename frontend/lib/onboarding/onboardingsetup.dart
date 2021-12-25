import 'package:flutter/material.dart';
import 'onboarding.dart';

class OnboardingScreen extends StatelessWidget {
  OnboardingScreen({Key? key}) : super(key: key);
  final onboardingPagesList = [
    Pages(
      widget: Column(
        children: [
          Container(
              padding: const EdgeInsets.only(top: 50, left: 10.0, right: 10.0),
              child: Image.asset(
                  'assets/coronasafe_full_logo_black_background.png')),
          Container(
              padding: const EdgeInsets.only(
                  bottom: 5, top: 20, left: 10, right: 50),
              width: double.infinity,
              child: const Text('Worried About Covid?',
                  style: TextStyle(
                    fontSize: 25,
                    fontFamily: 'CenturyGothic',
                    color: Colors.white,
                  ))),
          Container(
            padding: const EdgeInsets.only(bottom: 20, left: 10, right: 50),
            width: double.infinity,
            child: const Text(
              'We Get It',
              style: TextStyle(
                fontFamily: 'CenturyGothic',
                fontSize: 15,
                color: Color(0xF86BBBDF),
              ),
            ),
          ),
        ],
      ),
    ),
    Pages(
      widget: Column(
        children: [
          Container(
              padding: const EdgeInsets.only(top: 50, left: 10.0, right: 10.0),
              child: Image.asset(
                  'assets/coronasafe_full_logo_black_background.png')),
          Container(
              padding: const EdgeInsets.only(
                  bottom: 5, top: 20, left: 10, right: 50),
              width: double.infinity,
              child: const Text('We Get It',
                  style: TextStyle(
                    fontFamily: 'CenturyGothic',
                    fontSize: 25,
                    color: Colors.white,
                  ))),
          Container(
            padding: const EdgeInsets.only(bottom: 20, left: 10, right: 50),
            width: double.infinity,
            child: const Text(
              'That\'s why we made CoronaSafe, an app that calculates your risk of having contracted Covid-19',
              style: TextStyle(
                fontSize: 15,
                color: Color(0xF86BBBDF),
                fontFamily: 'CenturyGothic',
              ),
            ),
          ),
        ],
      ),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blueGrey,
      ),
      home: Onboarding(
        backgroundColor: Colors.grey[800],
        pages: onboardingPagesList,
      ),
    );
  }
}
