module m
contains

function sum_plain(a) result(res)
	implicit none
	real(8), intent(in) :: a(:)
	real(8) :: res
	integer(4) :: i
	res = 0
	do i = 1, size(a)
		res = res + a(i)
	end do
end function

function sum_omp(a) result(res)
	implicit none
	real(8), intent(in) :: a(:)
	real(8) :: res
	integer(4) :: i
	res = 0
	!$omp parallel do reduction(+:res)
	do i = 1, size(a)
		res = res + a(i)
	end do
end function

subroutine max_by_bin(a, bins, res)
	implicit none
	real(8),    intent(in) :: a(:)
	integer(4), intent(in) :: bins(:,:)
	real(8),    intent(inout) :: res(:)
	integer(4) :: i
	!$omp parallel do
	do i = 1, size(res)
		res(i) = maxval(a(bins(1,i)+1:bins(2,i)))
	end do
end subroutine

end module
