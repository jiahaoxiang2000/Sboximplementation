`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    17:39:44 02/22/2023 
// Design Name: 
// Module Name:    sboxtable 
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
module sboxtable(data_in,data_out);
   input [4:0] data_in;
	reg [4:0] data_out;
	output [4:0] data_out;
	
	 always @(data_in)
	 
	  begin 
	    case (data_in)
			 5'b00000: 
				begin 
					data_out = 5'b00100;
				end
			 5'b00001: 
				begin 
					data_out = 5'b01011;
				end
			 5'b00010: 
				begin 
					data_out = 5'b11111;
				end
			 5'b00011: 
				begin 
					data_out = 5'b10100;
				end
			 5'b00100: 
				begin 
					data_out = 5'b11010;
				end
			 5'b00101: 
				begin 
					data_out = 5'b10101;
				end
			 5'b00110: 
				begin 
					data_out = 5'b01001;
				end
			 5'b00111: 
				begin 
					data_out = 5'b00010;
				end
			 5'b01000: 
				begin 
					data_out = 5'b11011;
				end
			 5'b01001: 
				begin 
					data_out = 5'b00101;
				end
			 5'b01010: 
				begin 
					data_out = 5'b01000;
				end
			 5'b01011: 
				begin 
					data_out = 5'b01100;
				end
			 5'b01100: 
				begin 
					data_out = 5'b11101;
				end
			 5'b01101: 
				begin 
					data_out = 5'b00011;
				end
			 5'b01110: 
				begin 
					data_out = 5'b00110;
				end
			 5'b01111: 
				begin 
					data_out = 5'b11100;
				end	
			 5'b10000: 
				begin 
					data_out = 5'b11110;
				end
			 5'b10001: 
				begin 
					data_out = 5'b10011;
				end
			 5'b10010: 
				begin 
					data_out = 5'b00111;
				end
			 5'b10011: 
				begin 
					data_out = 5'b01110;
				end
			 5'b10100: 
				begin 
					data_out = 5'b00000;
				end
			 5'b10101: 
				begin 
					data_out = 5'b01101;
				end
			 5'b10110: 
				begin 
					data_out = 5'b10001;
				end
			 5'b10111: 
				begin 
					data_out = 5'b11000;
				end
			 5'b11000: 
				begin 
					data_out = 5'b10000;
				end
			 5'b11001: 
				begin 
					data_out = 5'b01100;
				end
			 5'b11010: 
				begin 
					data_out = 5'b00001;
				end
			 5'b11011: 
				begin 
					data_out = 5'b11001;
				end
			 5'b11100: 
				begin 
					data_out = 5'b10110;
				end
			 5'b11101: 
				begin 
					data_out = 5'b01010;
				end
			 5'b11110: 
				begin 
					data_out = 5'b01111;
				end
			 5'b11111: 
				begin 
					data_out = 5'b10111;
				end	
		endcase;
	end

endmodule
