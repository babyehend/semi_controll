import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:semi_controll/parameter.dart';

class PageExit extends StatefulWidget {
  const PageExit({super.key});

  @override
  State<PageExit> createState() => _PageExitState();
}

class _PageExitState extends State<PageExit> {
  @override
  Widget build(BuildContext context) {
    dynamic prov_para = Provider.of<parameter>(context);
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Flexible(
          flex: 1,
          child: Container(
            width: double.infinity,
            alignment: Alignment.topCenter,
            child: Text(
              "Exit",
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        Flexible(
          flex: 2,
          child: SizedBox(
            height: double.infinity,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Container(
                  width: 300,
                  height: 80,
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      await Dio().get('http://127.0.0.1:5000/exit');

                      setState(() {
                        exit(0);
                      });
                    },
                    icon: Icon(
                      Icons.cancel,
                      size: 40,
                      color: prov_para.textClr,
                    ),
                    label: Text(
                      "Exit",
                      style: TextStyle(
                        fontSize: 18,
                        color: prov_para.textClr,
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: prov_para.mainClr,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                  ),
                ),
                Container(
                  width: 300,
                  height: 80,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      prov_para.pageUpdate(0);
                    },
                    icon: Icon(
                      Icons.cancel,
                      size: 40,
                      color: prov_para.textClr,
                    ),
                    label: Text(
                      "Cancle",
                      style: TextStyle(
                        fontSize: 18,
                        color: prov_para.textClr,
                      ),
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: prov_para.mainClr,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        Flexible(
          flex: 1,
          child: SizedBox(
            height: double.infinity,
          ),
        ),
      ],
    );
  }
}
