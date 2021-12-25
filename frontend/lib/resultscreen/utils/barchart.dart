import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:coronasafe/utils/place.dart';

class MyBarChart extends StatelessWidget {
  const MyBarChart({Key? key, required this.place}) : super(key: key);
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
      swapAnimationDuration: const Duration(milliseconds: 1000),
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
                borderRadius: const BorderRadius.all(Radius.circular(10)),
                y: place.percentage,
                colors: [Colors.greenAccent, Colors.yellow, Colors.redAccent])
          ],
          showingTooltipIndicators: [0],
        ),
      ];
}
