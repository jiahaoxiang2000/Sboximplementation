`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    21:34:50 02/22/2023 
// Design Name: 
// Module Name:    newAscon 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module newAscon(
    input data_in0,
    input data_in1,
    input data_in2,
    input data_in3,
    input data_in4,
    output data_out0,
    output data_out1,
    output data_out2,
    output data_out3,
    output data_out4
    );
	 wire t0,t1,t3,t4,t7,t8,t9,t10;
	 moai m0(data_in1,data_in0,data_in1,data_in4,t0);
	 moai m1(data_in2,data_in1,data_in2,data_in1,t1);
	 moai m2(data_in3,t0,data_in3,t0,data_out4);
	 moai m3(data_in4,data_in0,data_in3,data_in0,t3);
	 moai m4(t1,data_in4,t1,data_in4,t4);
	 moai m5(t3,t4,t3,t4,data_out3);
	 moai m6(t1,data_in3,t4,data_in3,data_out2);
	 moai m7(data_in3,data_in2,data_in3,data_in2,t7);
	 moai m8(t4,t7,t4,t7,t8);
	 not n0(t9,data_in0);
	 moai m9(t9,t8,t9,t8,data_out1);
	 moai m10(t4,data_in1,t9,data_in1,t10);
	 moai m11(t7,t10,t7,t10,data_out0);

endmodule

module moai(data_in0,data_in1,data_in2,data_in3,data_out);
	input data_in0;
    input data_in1;
    input data_in2;
    input data_in3;
    output data_out;
	 
	 wire t0,t1,t2,t3;
	 and a0(t0, data_in1, data_in0);
	 not n0(t1, t0);
	 or  o0(t2, data_in3, data_in2);
	 and a1(t3, t1, t2);
	 not n1(data_out, t3);
endmodule
