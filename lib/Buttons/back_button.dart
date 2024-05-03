import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:semi_controll/parameter.dart';

class BackButton extends StatefulWidget {
  const BackButton({super.key});

  @override
  State<BackButton> createState() => _BackButtonState();
}

class _BackButtonState extends State<BackButton> {
  @override
  Widget build(BuildContext context) {
    dynamic prov_para = Provider.of<parameter>(context);
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        color: prov_para.mainClr,
      ),
      child: IconButton(
        onPressed: () {
          prov_para.pageUpdate(0);
        },
        icon: Icon(
          prov_para.back,
          size: 28,
        ),
      ),
    );
  }
}
