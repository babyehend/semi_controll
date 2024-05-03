import 'package:flutter/material.dart';
import 'package:semi_controll/Buttons/back_button.dart' as myback;
import 'Pannels/status_pannel.dart';

class PageManual extends StatefulWidget {
  const PageManual({super.key});

  @override
  State<PageManual> createState() => _PageManualState();
}

class _PageManualState extends State<PageManual> {
  @override
  Widget build(BuildContext context) {
    return const Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Flexible(
          flex: 1,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              myback.BackButton(),
              Text(
                "Manual Controll",
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(),
            ],
          ),
        ),
        Flexible(
          flex: 4,
          child: SizedBox(
            height: double.infinity,
            child: Column(
              children: [
                Row(
                  children: [
                    PannelHMDS(),
                    PannelSpin(),
                    PannelExpos(),
                  ],
                ),
                Row(
                  children: [
                    PannelDevel(),
                    PannelBake(),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
