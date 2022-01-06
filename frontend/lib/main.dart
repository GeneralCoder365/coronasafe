import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import './onboarding/onboardingcontrol.dart';

main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const CheckOnboarding(),
      theme: ThemeData(fontFamily: 'Manrope'),
    );
  }
}
