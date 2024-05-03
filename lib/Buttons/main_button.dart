import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:semi_controll/parameter.dart';

class MainButton extends StatefulWidget {
  const MainButton({
    super.key,
    required this.icon,
    required this.text,
    required this.index,
  });

  final IconData icon;
  final String text;
  final int index;

  @override
  State<MainButton> createState() => _MainButtonState();
}

class _MainButtonState extends State<MainButton> {
  @override
  Widget build(BuildContext context) {
    dynamic prov_para = Provider.of<parameter>(context);
    return Container(
      margin: const EdgeInsets.all(10),
      width: double.infinity,
      height: 80,
      child: ElevatedButton.icon(
        onPressed: () {
          prov_para.pageUpdate(widget.index);
        },
        icon: Icon(
          widget.icon,
          size: 40,
          color: prov_para.textClr,
        ),
        label: Text(
          widget.text,
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
    );
  }
}
