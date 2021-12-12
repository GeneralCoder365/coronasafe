import 'package:flutter/material.dart';
import 'main.dart';
import 'onboarding.dart';
import 'onboardingsetup.dart';
import 'package:after_layout/after_layout.dart';
import 'package:shared_preferences/shared_preferences.dart';

class CheckOnboarding extends StatefulWidget {
  const CheckOnboarding({Key? key}) : super(key: key);

  @override
  CheckOnboardingState createState() => CheckOnboardingState();
}

class CheckOnboardingState extends State<CheckOnboarding>
    with AfterLayoutMixin<CheckOnboarding> {
  Future checkFirstSeen() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    bool _seen = (prefs.getBool('seen') ?? false);

    if (_seen) {
      Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => const MyHomePage()));
    } else {
      await prefs.setBool('seen', true);
      Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => OnboardingScreen()));
    }
  }

  @override
  void afterFirstLayout(BuildContext context) => checkFirstSeen();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[800],
      body: const Center(
        child: Text('Loading...'),
      ),
    );
  }
}
